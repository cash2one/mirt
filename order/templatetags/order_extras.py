# -*- coding: utf-8 -*-
from django import template

from catalog.models import WebStock

register = template.Library()

from order.cart import ShoppingCart


@register.inclusion_tag('order/tags/cart_widget.html', takes_context=True)
def cart_tag(context):
    cart = ShoppingCart(context.get('request'))
    return {'cart': cart }


@register.inclusion_tag('order/tags/cart_widget_old.html', takes_context=True)
def cart_tag_old(context):
    cart = ShoppingCart(context.get('request'))
    return {'cart': cart }


@register.inclusion_tag('order/tags/webstocks.html', takes_context=True)
def stocks_tag(context):
    opts = list(WebStock.objects.all())
    return {'opts': opts}

