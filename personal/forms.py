# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from personal.models import UserProfile

attrs_dict = {'class': 'required'}


def validate_phone(value):
    if not re.match("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{6,10}", value):
        raise ValidationError(u'%s не является правильным номером' % value)


def validate_email(value):
    if not re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", value):
        raise ValidationError(u'%s не является корректным email' % value)


class ResetForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label="Email",
                             validators=[validate_email])


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label="Email")
    first_name = forms.CharField(label=u"Имя")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label="Пароль (повтор)")

    def clean_email(self):
        existing = User.objects.filter(
            Q(email__iexact=self.cleaned_data['email']) | Q(username__iexact=self.cleaned_data['email']))
        if existing.exists():
            raise forms.ValidationError(u"Этот email адрес уже используется.")
        else:
            return self.cleaned_data['email'].lower()

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u"Пароли не совпадают.")
        return self.cleaned_data

    def clean_password1(self):
        if 'password1' in self.cleaned_data:
            if len(self.cleaned_data['password1']) < 5:
                raise forms.ValidationError(u"Пароль слишком короткий (пароль должен быть не менее 5 символов).")
        return self.cleaned_data['password1']


class AuthenticationForm(forms.Form):
    username = forms.CharField(label=u"Email", max_length=30)
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': u"Укажите корректные email и пароль. Поле пароля чувствительно к регистру символов.",
        'no_cookies': u"Ваш браузер не поддерживает cookies. Cookies необходимы для входа.",
        'inactive': u"Эта учетная запись отключена.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username:
            username = username.lower()

        if username and password:
            try:
                user = User.objects.get(email = username)
                username = user.username
            except:
                pass
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',)


class EditUserProfileForm(forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone], label=u"Телефон", required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)
