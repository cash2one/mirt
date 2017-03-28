# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
import re
from message.models import Message
from random import choice


register = template.Library()


@register.inclusion_tag('templatetags/feedback_form.html')
def feedback_form(request, context=None):
    show_form = False
    if "show_form" in request.GET or "show_form" in request.POST:
        show_form = True

    if 'thanks_for_feedback' in request.GET:
        show_form = True
        mess ="<p>спасибо</p>"
        try:
            mess = Message.objects.filter(type='message_after_feedback_form')[0].message
        except:
            pass
        context = {"mess": mess,
                   "success": True}

    return {'context': context, 'show_form': show_form }