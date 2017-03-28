# -*- coding: utf-8 -*-
import datetime
from django import template
from django.conf import settings

from data_exchange.models import DataExchange
from flatpages.models import FlatPage, IndexPage, Advantage
import re
# from message.models import Message
from random import choice

register = template.Library()


class FlatpageNode(template.Node):
    def __init__(self, context_name, starts_with=None, user=None):
        self.context_name = context_name
        if starts_with:
            self.starts_with = template.Variable(starts_with)
        else:
            self.starts_with = None
        if user:
            self.user = template.Variable(user)
        else:
            self.user = None

    def render(self, context):
        flatpages = FlatPage.objects.filter(sites__id=settings.SITE_ID)
        # If a prefix was specified, add a filter
        if self.starts_with:
            flatpages = flatpages.filter(
                url__startswith=self.starts_with.resolve(context))

        # If the provided user is not authenticated, or no user
        # was provided, filter the list to only public flatpages.
        if self.user:
            user = self.user.resolve(context)
            if not user.is_authenticated():
                flatpages = flatpages.filter(registration_required=False)
        else:
            flatpages = flatpages.filter(registration_required=False)

        context[self.context_name] = flatpages
        return ''


def get_flatpages(parser, token):
    """
    Retrieves all flatpage objects available for the current site and
    visible to the specific user (or visible to all users if no user is
    specified). Populates the template context with them in a variable
    whose name is defined by the ``as`` clause.

    An optional ``for`` clause can be used to control the user whose
    permissions are to be used in determining which flatpages are visible.

    An optional argument, ``starts_with``, can be applied to limit the
    returned flatpages to those beginning with a particular base URL.
    This argument can be passed as a variable or a string, as it resolves
    from the template context.

    Syntax::

        {% get_flatpages ['url_starts_with'] [for user] as context_name %}

    Example usage::

        {% get_flatpages as flatpages %}
        {% get_flatpages for someuser as flatpages %}
        {% get_flatpages '/about/' as about_pages %}
        {% get_flatpages prefix as about_pages %}
        {% get_flatpages '/about/' for someuser as about_pages %}
    """
    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['url_starts_with'] [for user] as context_name" %
                      dict(tag_name=bits[0]))
    # Must have at 3-6 bits in the tag
    if len(bits) >= 3 and len(bits) <= 6:

        # If there's an even number of bits, there's no prefix
        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None

        # The very last bit must be the context name
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        # If there are 5 or 6 bits, there is a user defined
        if len(bits) >= 5:
            if bits[-4] != 'for':
                raise template.TemplateSyntaxError(syntax_message)
            user = bits[-3]
        else:
            user = None

        return FlatpageNode(context_name, starts_with=prefix, user=user)
    else:
        raise template.TemplateSyntaxError(syntax_message)

register.tag('get_flatpages', get_flatpages)


@register.inclusion_tag('templatetags/../../templates/templatetags/text_ext.html')
def get_index_text(bottom=None):
    try:
        # if bottom:
        #     return {'content': IndexPage.objects.all()[0].seo_text}
        # else:
        return {'content': IndexPage.objects.all()[0].content}
    except:
        return {'content': 'NoneIndexPage'}


@register.inclusion_tag('templatetags/top_menu.html')
def get_top_menu(url=''):
    nodes = FlatPage.objects.filter(show_in_menu=True, is_visible=True, parent=None)
    return {'nodes': nodes, 'url': url}


# old
@register.inclusion_tag('templatetags/top_menu_old.html')
def get_top_menu_old(url=''):
    nodes = FlatPage.objects.filter(show_in_menu=True, is_visible=True, parent=None)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/top_menu_mobile.html')
def get_top_menu_mobile(url=''):
    nodes = FlatPage.objects.filter(show_in_menu=True, is_visible=True, parent=None)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/bottom_menu.html')
def get_bottom_menu(url=''):
    nodes = FlatPage.objects.filter(show_in_bottom_menu=True, is_visible=True)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/bottom_menu_old.html')
def get_bottom_menu_old(url=''):
    nodes = FlatPage.objects.filter(show_in_bottom_menu=True, is_visible=True)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('flatpages/templatetags/sub_bottom_menu.html')
def get_sub_bottom_menu(url=''):
    source_nodes = FlatPage.objects.filter(show_in_sub_bottom_menu=True, is_visible=True)
    root_indexes = []
    nodes = []
    for index, item in enumerate(source_nodes):
        if item.parent:
            root = next((i for i in source_nodes if i == item.parent), None)
            if root:
                if not hasattr(root, "children"):
                    root.children = []
                root.children.append(item)
        else:
            root_indexes.append(index)

    for i in root_indexes:
        nodes.append(source_nodes[i])

    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('flatpages/templatetags/sub_bottom_menu_old.html')
def get_sub_bottom_menu_old(url=''):
    source_nodes = FlatPage.objects.filter(show_in_sub_bottom_menu=True, is_visible=True)
    root_indexes = []
    nodes = []
    for index, item in enumerate(source_nodes):
        if item.parent:
            root = next((i for i in source_nodes if i == item.parent), None)
            if root:
                if not hasattr(root, "children"):
                    root.children = []
                root.children.append(item)
        else:
            root_indexes.append(index)

    for i in root_indexes:
        nodes.append(source_nodes[i])

    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/side_menu.html')
def flatpages_side_menu(url=''):
    expand = []
    if url:
        pages = FlatPage.objects.filter(url=url)
        if pages:
            page = pages[0]
            for item in page.get_ancestors(include_self=True):
                if not item.is_leaf_node():
                    expand.append(item.url)
    nodes = FlatPage.tree.filter(show_in_side_menu=True, is_visible=True)
    return {'nodes': nodes, 'url': url, 'expand': expand}


@register.inclusion_tag('flatpages/templatetags/advantages.html')
def get_advantages():
    items = Advantage.objects.filter(is_visible_on_main=True, is_visible=True)
    return {"items": items}
#
#
# @register.inclusion_tag('templatetags/../../templates/templatetags/mobile.html')
# def is_mobile(request):
#     is_mobile = False
#     try:
#         user_agent = request.META.get("HTTP_USER_AGENT")
#         expression = 'Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|Kindle|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune'
#
#         if re.search(expression, user_agent):
#             is_mobile = True
#     except:
#         pass
#     return {'is_mobile': is_mobile }

@register.simple_tag(takes_context=False)
def get_last_date():
    timefinish = DataExchange.objects.get(type='importing_prices').time_finish
    return datetime.datetime.strftime(timefinish, "%Y-%m-%d %H:%M:%S")