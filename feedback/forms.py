#-*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
import re

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = u'Это поле обязательно!'
            if 'invalid' in field.error_messages:
                field.error_messages['invalid'] = u'Это поле заполнено неверно!'


def validate_phone(value):
    if not re.match("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{6,10}", value):
        raise ValidationError(u'%s не является правильным номером' % value)

def validate_email(value):
    if not re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", value):
        raise ValidationError(u'%s не является корректным email' % value)


class FeedbakForm(CustomForm):
    eman = forms.CharField(max_length=255,)
    email = forms.CharField(validators=[validate_email])
    message = forms.CharField(max_length=1000, )