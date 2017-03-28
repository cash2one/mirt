# -*- coding: utf-8 -*-

from django import template
from slider.models import Slide

register = template.Library()

@register.inclusion_tag('templatetags/slider.html')
def slider():
    s = list(Slide.objects.filter(show=True))
    show_buttons = True

    if s:
        if len(s) < 2:
            show_buttons = False
        return {'slides': s, "show_buttons": show_buttons}
    else:
        return {'slides': None}
