# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from registration.views import activate
from personal.forms import RegistrationForm

urlpatterns = patterns('',
    url(r'^activate/success/$', 'personal.views.activation_complete', name='activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate, {'backend': 'personal.backend.RegistrationBackend', 'success_url': 'personal:activation_complete', 'template_name': 'index.html'}, name='registration_activate'),

    url(r'^register/$', 'personal.views.register', {
        'backend': 'personal.backend.RegistrationBackend',
        'form_class': RegistrationForm
    }, name='registration_register'),
)
