# -*- coding: utf-8 -*-
import base64
import pickle
from django import template
from django.core.urlresolvers import reverse

from personal.forms import AuthenticationForm, RegistrationForm, ResetForm

register = template.Library()


@register.inclusion_tag('templatetags/auth_tag.html')
def auth_form(request):
    name = ''
    data = {'no_enter': False}
    if request.user.is_anonymous():
        data['no_enter'] = True
        data['hide'] = 'block;'
        if request.GET.get('registr', None):
            data['form'] = RegistrationForm()
            data['action_to'] = reverse('personal:registration_register')
            data['name'] = u'Регистрация'
            data['submit_name'] = u'Зарегистрироваться'
            data['extra_links']=[{'q':'auth','name':u'Авторизация'},{'q':'remind','name':u'Востановление пароля'}]

        elif request.GET.get('remind', None):
            data['form'] = ResetForm()
            data['action_to'] = reverse('personal:password_reset')
            data['name'] = u'Востановление пароля'
            data['submit_name'] = u'Востановить'
            data['extra_links']=[{'q':'auth','name':u'Авторизация'},{'q':'registr','name':u'Регистрация'}]
        else:
            if not request.GET.get('auth', None):
                data['hide'] = 'none;'

            data['form'] = AuthenticationForm()
            data['action_to'] = reverse('personal:auth_login')
            data['name'] = u'Авторизация'
            data['submit_name'] = u'Авторизироваться'
            data['extra_links']=[{'q':'registr','name':u'Регистрация'},{'q':'remind','name':u'Востановление пароля'}]
    else:
        name = request.user.first_name

    if 'form' in request.session:
        form = request.session['form']
        data['form'] = form
        del request.session['form']

    return {'data':data,'name':name}


@register.inclusion_tag('templatetags/auth_tag_old.html')
def auth_form_old(request):
    name = ''
    data = {'no_enter': False}
    if request.user.is_anonymous():
        data['no_enter'] = True
        data['hide'] = 'block;'
        if request.GET.get('registr', None):
            data['form'] = RegistrationForm()
            data['action_to'] = reverse('personal:registration_register')
            data['name'] = u'Регистрация'
            data['submit_name'] = u'Зарегистрироваться'
            data['extra_links']=[{'q':'auth','name':u'Авторизация'},{'q':'remind','name':u'Востановление пароля'}]

        elif request.GET.get('remind', None):
            data['form'] = ResetForm()
            data['action_to'] = reverse('personal:password_reset')
            data['name'] = u'Востановление пароля'
            data['submit_name'] = u'Востановить'
            data['extra_links']=[{'q':'auth','name':u'Авторизация'},{'q':'registr','name':u'Регистрация'}]
        else:
            if not request.GET.get('auth', None):
                data['hide'] = 'none;'

            data['form'] = AuthenticationForm()
            data['action_to'] = reverse('personal:auth_login')
            data['name'] = u'Авторизация'
            data['submit_name'] = u'Авторизироваться'
            data['extra_links']=[{'q':'registr','name':u'Регистрация'},{'q':'remind','name':u'Востановление пароля'}]
    else:
        name = request.user.first_name

    if 'form' in request.session:
        form = request.session['form']
        data['form'] = form
        del request.session['form']

    return {'data':data,'name':name}
