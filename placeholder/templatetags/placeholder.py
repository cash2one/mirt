# -*- coding: utf-8 -*-

from django import template
from django.core.cache import cache
from ..models import Placeholder

register = template.Library()
CACHE_PREFIX = 'placeholder_'

def placeholder_parser(parser, token):
    cache_time = 0
    key = []
    tokens = token.split_contents()
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)

    if len(tokens) == 2:
        tag_name, key = tokens

    if len(tokens) == 3:
        tag_name, key, cache_time = tokens

    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    return PlaceholderNode(key[1:-1], cache_time)

class PlaceholderNode(template.Node):
    def __init__(self, key, cache_time=0):
        self.key = key
        self.cache_time = cache_time

    def render(self, context):
        try:
            cache_key = CACHE_PREFIX + self.key
            c = cache.get(cache_key)
            if c is None:
                c = Placeholder.objects.get(name=self.key)
                cache.set(cache_key, c, int(self.cache_time))
            content = c.content
        except Placeholder.DoesNotExist:
            content = ''
        return content

register.tag('placeholder', placeholder_parser)