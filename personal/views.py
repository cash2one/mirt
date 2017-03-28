# -*- coding: utf-8 -*-
import base64
import pickle
from constance import config
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site, Site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import loader, Context, Template
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.utils.http import int_to_base36, base36_to_int
from registration.backends import get_backend
from registration.signals import user_registered, user_activated
from registration.models import RegistrationProfile
from main.views import simple_pagination
from order.models import Order
from personal.forms import AuthenticationForm, EditUserProfileForm, EditUserForm, ResetForm
from personal.models import UserProfile
import json
from message.models import Mail


def send_activation_email(sender, user, request, **kwargs):
    registration_profile = RegistrationProfile.objects.get(user=user)
    activation_key = registration_profile.activation_key

    context = {
        'user': user,
        'site': Site.objects.get_current(),
        'activation_key': activation_key
    }
    try:
        subject = request.activation_email.subject
        html_content = Template(request.activation_email.mail).render(Context(context))
        msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
        msg.content_subtype = "html"
        msg.send()

    except Exception, e:
        text = 'Не заполненое уведомление на почту. об отправке письма для активации %s' % e
        subject = 'Ошибка настройки сайта bshop'
        html_content = render_to_string('text.html', {'context': text})
        msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
        msg.content_subtype = "html"
        msg.send()


user_registered.connect(send_activation_email)


def send_account_activated_email(sender, user, request, **kwargs):
    context = {
        'user': user,
        'site': Site.objects.get_current()
    }

    try:
        subject = request.account_activated_email.subject
        html_content = Template(request.account_activated_email.mail).render(Context(context))

        msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
        msg.content_subtype = "html"
        msg.send()
    except Exception, e:
        text = 'Не заполненое уведомление на почту. об успешной активации. %s' % e
        subject = 'Ошибка настройки сайта bshop'
        html_content = render_to_string('text.html', {'context': text})
        msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
        msg.content_subtype = "html"
        msg.send()


user_activated.connect(send_account_activated_email)


def register(request, backend, form_class=None):
    backend = get_backend(backend)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                messages.success(request, request.message_after_activation_email)
            except:
                messages.success(request,
                                 u'Вы успешно зарегистрированны, на Ваш почтовый ящик направленно письмо с информацией')

            user = backend.register(request, **form.cleaned_data)
            user_reg = User.objects.get(email=form.cleaned_data['email'])
            try:
                profile = user_reg.profile
                profile.save()
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user_reg)
                profile.save()

        else:
            try:
                messages.success(request, request.message_after_error_reg)
            except:
                messages.success(request, u'Что то пошло не так')
            request.session['form'] = form
            return HttpResponseRedirect('/?registr=True')
    return HttpResponseRedirect('/')


def activation_complete(request):
    try:
        messages.success(request, request.message_after_successful_authentication)
    except:
        messages.success(request, u'Аккаунт успешно активированн')
    return HttpResponseRedirect('/')


@csrf_protect
def login(request, authentication_form=AuthenticationForm):
    where = "/"
    if request.META.get('HTTP_REFERER'):
        where = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            try:
                messages.success(request, request.message_after_successful_authentication)
            except:
                messages.success(request, u'Добро пожаловать')
        else:
            try:
                messages.success(request, request.message_novalid_authentication)
            except:
                messages.success(request, u'Неверно введён логин или пароль')
            request.session['form'] = form
            return HttpResponseRedirect('/?auth=True')
    where = where.replace('/?auth=True', '')
    next_page = request.GET.get('next', where)
    if next_page:
        where = next_page
    return HttpResponseRedirect(where)


def logout(request):
    auth_logout(request)
    try:
        messages.success(request, request.message_logout)
    except:
        messages.success(request, u'Досвидания')
    try:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return HttpResponseRedirect('/')


@login_required
def edit_user_profile(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    form = EditUserForm(request.POST or None, instance=user)
    profile_form = EditUserProfileForm(request.POST or None, instance=profile)
    email = user.email
    if request.method == 'POST':
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            try:
                messages.success(request,request.messages_good_edit)
            except:
                messages.success(request, u'Данные успешно сохранены')
    breadcrumbs = [{'url': reverse('personal:edit_user_profile'), 'title': 'Личный кабинет'}, ]
    return render(request, 'personal/profile_edit.html',
                  {'form': form, 'profile_form': profile_form, 'email': email, 'breadcrumbs': breadcrumbs})


@login_required
def edit_password(request):
    user = request.user
    norepeat = False
    novalid = False
    if request.method == "POST":
        oldpass = request.POST.get("oldpass")
        newpass = request.POST.get("newpass")
        cnewpass = request.POST.get("cnewpass")
        user_cache = authenticate(username=user.username, password=oldpass)
        if not (user_cache is None):
            if newpass == cnewpass:
                user.set_password(newpass)
                user.save()
                try:
                    messages.success(request, request.message_after_successful_password_changing)
                except:
                    messages.success(request, u'Данные успешно сохранены')
            else:
                norepeat = True
                try:
                    messages.success(request, request.messages_pass_not_confirm)
                except:
                    messages.success(request, u'Не совпадает пароли')
        else:
            novalid = True
            try:
                messages.success(request, request.messages_not_valid_password)
            except:
                messages.success(request, u'Введён неверный пароль')

    form = EditUserForm(None, instance=user)
    profile_form = EditUserProfileForm(None, instance=user.profile)
    email = user.email
    breadcrumbs = [{'url': reverse('personal:edit_user_profile'), 'title': 'Личный кабинет'},
                   ]

    return render(request, 'personal/profile_edit.html', {'form': form, 'novalid': novalid, 'norepeat': norepeat,
                                                          'profile_form': profile_form, 'email': email,
                                                          'breadcrumbs': breadcrumbs})


@csrf_protect
def password_reset(request):
    form = ResetForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            email = request.POST.get("email")
            try:
                user = User.objects.filter(Q(Q(username=email) | Q(email=email)))[0]
            except:
                user = None

            if not (user is None):
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain

                context = {
                    'domain': domain,
                    'site_name': site_name,
                    'uid': int_to_base36(user.id),
                    'token': default_token_generator.make_token(user),
                }
                try:
                    messages.success(request, request.message_after_password_reset_email)
                except:
                    messages.success(request, u'На указанную почту (%s) отправленно сообщение с инструкцией' % email)
                try:

                    subject = Mail.objects.get(type='password_reset_email').subject
                    html_content = Template(Mail.objects.get(type='password_reset_email').mail).render(Context(context))
                    msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
                    msg.content_subtype = "html"
                    msg.send()

                except:
                    text = 'Не заполненое уведомление на почту. об отправке письма для восстановления пароля'
                    subject = 'Ошибка'
                    html_content = render_to_string('text.html', {'context': text})
                    msg = EmailMessage(subject, html_content, config.EMAIL_FROM, [user.email])
                    msg.content_subtype = "html"
                    msg.send()
        else:
            try:
                messages.success(request, request.messages_email_not_found)
            except:
                messages.success(request, u'Адрес электронной почты не зарегистрирован')
            request.session['form'] = form
            return HttpResponseRedirect('/?remind=True')

    return HttpResponseRedirect('/')


def password_reset_confirm(request, uidb36=None, token=None):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, OverflowError, User.DoesNotExist):
        user = None

    breadcrumbs = [{'url': reverse('personal:edit_user_profile'), 'title': 'Личный кабинет'}, ]
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            newpass = request.POST.get("newpass")
            cnewpass = request.POST.get("cnewpass")
            if newpass == cnewpass:
                user.set_password(newpass)
                user.save()
                try:
                    messages.success(request, request.message_after_successful_password_changing)
                except:
                    messages.success(request, u'Сообщение об успешной смене пароля незаполнено')
                return redirect('/')

            else:
                try:
                    messages.success(request, request.messages_pass_not_confirm)
                except:
                    messages.success(request, u'Введённые пароли не совпадают')
    return render(request, 'personal/reset.html', {'breadcrumbs': breadcrumbs})

    # return redirect('/?uidb36=%s&token=%s' % (uidb36, token))


@login_required
def list_orders(request):
    user = request.user
    per_page = int(config.ORDERS_ON_PAGE)
    orders = simple_pagination(request, list(Order.objects.filter(email=user.email).order_by('-id')), per_page)
    breadcrumbs = [{'url': reverse('personal:edit_user_profile'), 'title': 'Личный кабинет'},
                   {'url': '', 'title': 'История покупок'},
                   ]
    return render(request, 'personal/order_list.html', {'orders': orders, 'breadcrumbs': breadcrumbs})
