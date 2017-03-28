# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('order.views',
    url(r'^$', 'checkout', name='checkout'),
    url(r'^add/(?P<product_id>\d+)/$', 'add_to_cart', name='add_to_cart'),
    url(r'^remove/(?P<item_id>\d+)/$', 'remove_from_cart', name='remove_from_cart'),
    url(r'^update/(?P<item_id>\d+)/(?P<quantity>[\d-]+)', 'update_cart', name='update_cart'),
    # url(r'^clear/$', 'clear_cart', name='clear_cart'),
    url(r'^$', 'get_cart', name='cart'),
)