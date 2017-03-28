# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from feincms.admin import tree_editor
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse
from quick_links.models import QuickLink, \
    QuickProductLink, \
    QuickDirectoryLink, \
    QuickBrandLink, \
    ProductGroup, \
    ProductFromGroup, \
    QuickGroupLink

from simpleseo.admin import seo_inline
from django.contrib.admin.actions import delete_selected as delete_selected_item
class ProductGroupInline(admin.TabularInline):
    model = ProductGroup
    extra = 0


class ProductFromGroupInline(admin.TabularInline):
    extra = 0
    model = ProductFromGroup
    raw_id_fields = ('product',)
    autocomplete_lookup_fields = {
    'fk': ['product'],}


class ProductGroupAdmin(admin.ModelAdmin):
    inlines = [ProductFromGroupInline]
admin.site.register(ProductGroup, ProductGroupAdmin)


class QuickProductGroupInline(admin.TabularInline):
    extra = 0
    model = QuickGroupLink
    raw_id_fields = ('group',)
    autocomplete_lookup_fields = {
    'fk': ['group'],}

class QuickProductlinkInline(admin.TabularInline):
    extra = 0
    model = QuickProductLink
    raw_id_fields = ('product',)
    autocomplete_lookup_fields = {
    'fk': ['product'],}


class QuickDirectorylinkInline(admin.TabularInline):
    model = QuickDirectoryLink
    extra = 0
    raw_id_fields = ('directory',)
    autocomplete_lookup_fields = {
    'fk': ['directory'],}


class QuickBrandlinkInline(admin.TabularInline):
    model = QuickBrandLink
    extra = 0
    raw_id_fields = ('brand',)
    autocomplete_lookup_fields = {
    'fk': ['brand'],}



class QuicklinkAdmin(tree_editor.TreeEditor):
    list_display = ('name', 'order', 'is_visible', 'parent')
    list_editable = ('order','is_visible')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [QuickProductlinkInline,
               QuickDirectorylinkInline,
               QuickBrandlinkInline,
               QuickProductGroupInline,
               seo_inline()]

    def get_actions(self, request):
        actions = super(QuicklinkAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (delete_selected_item, 'delete_selected', u"Удалить выбранные страницы сайта")
        return actions

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('description_up',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Текст над товарами', label=u'Верхнее описание', required=False)
        if db_field.name in ('description_down',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Текст под товарами', label=u'Нижнее описание', required=False)
        return super(QuicklinkAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(QuickLink, QuicklinkAdmin)