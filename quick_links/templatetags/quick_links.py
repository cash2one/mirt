# -*- coding: utf-8 -*-
from django import template
from ..models import QuickLink

register = template.Library()


class QuickLinkDisplayItem(object):
    def __init__(self, name, slug, id, active_id):
        is_active = lambda x: True if x == active_id else False
        self.name = name
        self.slug = slug
        self.active = is_active(id)
        self.children = []

    def add_child(self, item):
        self.children.append(item)
        if item.active:
            self.active = True


@register.inclusion_tag('quick_links/tags/quick_links_menu.html', takes_context=True)
def quick_links(context, active=None):
    # TODO: переписать, чтобы уменьшить количество запросов


    # Вот была бы QuickLink деревом, не пришлось бы изобретать ввелосипед

    # ну а пока используем вспомогательный класс QuickLinkDisplayItem
    # чтобы построить что-то наподобие

    # да знаю, можно было-бо рекурсивно пройтись, но по заданию нужно всего 3 уровня
    # поэтому расписываем всё влоб

    links = []
    all_links = QuickLink.objects.filter(is_visible=True)

    #сначала берём элементы, которые однозначно корневые
    for root_link in all_links.filter(parent=None).order_by("order")[:4]:
    # находим элементы уровня 0
        link_level_0 = QuickLinkDisplayItem(root_link.name, root_link.slug, root_link.id, active)
        for child in all_links.filter(parent=root_link).order_by("order").values_list("name", "slug", "id"):
        # находим элементы уровня 1
            link_level_1 = QuickLinkDisplayItem(child[0], child[1], child[2], active)
            for x_child in all_links.filter(parent__id=child[2]).order_by("order").values_list("name", "slug", "id"):
            # находим элементы уровня 2
                link_level_2 = QuickLinkDisplayItem(x_child[0], x_child[1], x_child[2], active)
                # заполняем уровень 2
                link_level_1.add_child(link_level_2)
            # заполняем уровень 1
            link_level_0.add_child(link_level_1)
        # заполняем уровень 0
        links.append(link_level_0)

    context['quick_links'] = links
    return context
