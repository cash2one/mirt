# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('personal.views',
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^logout/$', 'logout',  name='auth_logout'),
    url(r'^changepass/$', 'edit_password', name='edit_password'),
    url(r'^password_reset/$', 'password_reset', name='password_reset'),
    url(r'^orders/$', 'list_orders', name='list_orders'),
    url(r'^$', 'edit_user_profile', name='edit_user_profile'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm',
        name='password_reset_confirm'),

    url(r'^', include('personal.backend.urls')),
)