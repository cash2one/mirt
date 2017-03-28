# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('announce.views',
    url(r'^anonsy/$', 'announce_list', name='announce-list'),
    url(r'^anonsy/(?P<slug>([-\w]+))/$', 'announce_detail', name='announce-detail'),
)
