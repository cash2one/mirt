# -*- coding: utf-8 -*-

from django import template
from news.models import News
from constance import config

register = template.Library()


@register.inclusion_tag('templatetags/news_widget.html')
def news_widget():
    list = News.objects.filter(is_visible=True, is_visible_main=True).order_by('-created_at')[:config.NEWS_ON_MAIN]
    return {'list': list }
