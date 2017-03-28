# -*- coding: utf-8 -*-

from models import Mail, Message
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from main import settings

class MessageAdmin(admin.ModelAdmin):
    list_display = ('type',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'message':
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), label=u'Текст сообщения', required=False)
        return super(MessageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Message, MessageAdmin)


class MailAdmin(admin.ModelAdmin):
    list_display = ('type',)

    def has_add_permission(self, *args, **kwargs):
        if settings.DEBUG:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if settings.DEBUG:
            return True
        else:
            return False

admin.site.register(Mail, MailAdmin)