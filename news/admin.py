# -*- coding: utf-8 -*-

from news.models import News, Blog_Tag

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from simpleseo.admin import seo_inline


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'short_description', 'is_visible', 'is_visible_main',)
    list_editable = ('is_visible', 'is_visible_main',)
    list_filter = ('created_at', 'is_visible')
    list_display_links = ('title', 'created_at',)

    prepopulated_fields = {"slug": ("title",)}

    raw_id_fields = ('tags',)

    autocomplete_lookup_fields = {
        'm2m': ['tags'],}


    inlines = [seo_inline()]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('description',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Полный текст новости', label=u'Текст', required=False)

        return super(NewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(News, NewsAdmin)

class Blog_TagAdmin(admin.ModelAdmin):
    list_display = ('title','order',)
    list_editable = ('order',)

admin.site.register(Blog_Tag, Blog_TagAdmin)