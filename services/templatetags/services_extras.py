# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from services.models import Service
from random import choice

register = template.Library()

# @register.inclusion_tag('templatetags/../../templates/templatetags/top_menu.html')
# def get_top_menu(url=''):
#     nodes = FlatPage.objects.filter(show_in_menu=True, is_visible=True, parent=None)
#     return {'nodes': nodes, 'url': url}

@register.inclusion_tag('templatetags/side_menu.html')
def services_side_menu(url=''):
    expand = []
    if url:
        expand.append(url)
        for item in Service.objects.get(url=url).get_ancestors():
            expand.append(item.url)
    nodes = Service.tree.filter(is_visible=True)

    return {'nodes': nodes, 'url': url, 'expand': expand }

