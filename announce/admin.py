# -*- coding: utf-8 -*-

from models import Announce
from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from simpleseo.admin import seo_inline


class AnnounceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'teaser', 'is_visible','is_visible_on_main',)
    list_editable = ('is_visible','is_visible_on_main',)
    list_filter = ('created_at', 'is_visible','is_visible_on_main',)
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [seo_inline()]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('description',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Полный текст анонса', label=u'Текст', required=False)

        return super(AnnounceAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Announce, AnnounceAdmin)