# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from error_manag.models import ErrorMessage

class ErrorMessageAdmin(admin.ModelAdmin):
    list_display = ('type',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'message':
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), label=u'Текст сообщения', required=False)
        return super(ErrorMessageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(ErrorMessage, ErrorMessageAdmin)