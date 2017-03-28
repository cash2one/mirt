# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('catalog.views',
    url(r'^populyarnye-tovary/$', 'index_products', name='index-products'),
    url(r'^render_marker_data/(?P<id>\d+)/(?P<product_id>\d+)/$', 'render_marker_data', name='render-marker-data'),
    url(r'^all_(?P<type_promo>\w+)/$', 'list_promo_products', name='list_promo_products'),
    url(r'^analogi/(?P<id>[\d]+)/$', 'similar_products', name='simillar-products'),
    url(r'^(?P<slug>([-\w]+/){1,15})$', 'directory_detail_view', name='directory-detail'),
    url(r'^(?P<slug>([-\w]+/){1,15})(?P<item>[-\w]+)/$', 'product_detail_view', name='product-detail'),


)