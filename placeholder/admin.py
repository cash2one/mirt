# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse
from placeholder.models import Placeholder
from main import settings

class PlaceholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name', 'content')

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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('content',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Содержание плейсхолдера', label=u'Содержимое', required=False)
        return super(PlaceholderAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Placeholder, PlaceholderAdmin)