# -*- coding: utf-8 -*-

from django import template
from announce.models import Announce
from constance import config

register = template.Library()

@register.inclusion_tag('templatetags/announce_widget.html')
def announce_widget():
    list = Announce.objects.filter(is_visible=True, is_visible_on_main=True).order_by('-created_at')[:config.ANNOUNCES_ON_MAIN]
    return {'list': list }
