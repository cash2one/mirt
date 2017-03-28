# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('services.views',
    url(r'^uslugi/(?P<slug>([-\w]+))/$', 'service_detail', name='service-detail'),
)
