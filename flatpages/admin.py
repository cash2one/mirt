# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from feincms.admin import tree_editor
from tinymce.widgets import TinyMCE
from flatpages.models import FlatPage, IndexPage, Advantage
from main import settings
# незабываем импорт
from simpleseo.admin import seo_inline
from django.contrib.admin.actions import delete_selected as delete_selected_item


class FlatpageForm(forms.ModelForm):
    url = forms.RegexField(label='URL', max_length=100, regex=r'^[-\w/\.~]+$',
                           error_message=u"Значение должно состоять только из букв, цифр "
                                         u"и символов точки, подчеркивания, тире, косой черты и тильды.")
    content = forms.CharField(widget=TinyMCE, label=u'Содержимое', required=False)

    class Meta:
        model = FlatPage


class FlatPageAdmin(tree_editor.TreeEditor):
    form = FlatpageForm

    list_display = (
        'url',
        'type',
        'show_in_menu',
        'show_in_bottom_menu',
        'show_in_side_menu',
        'show_in_sub_bottom_menu',
        'is_visible',
        'order',
    )

    list_editable = (
        'show_in_menu',
        'show_in_bottom_menu',
        'show_in_sub_bottom_menu',
        'is_visible',
        'order',
        'show_in_side_menu',
    )

    search_fields = ('url', 'title')
    prepopulated_fields = {"url": ("title",)}
    #Тут втыкаем новое сео
    inlines = [seo_inline()]

    def get_actions(self, request):
        actions = super(FlatPageAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (delete_selected_item, 'delete_selected', u"Удалить выбранные страницы сайта")
        return actions


admin.site.register(FlatPage, FlatPageAdmin)


class AdvantageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    list_display = ('title', 'is_visible_on_main', 'is_visible', 'order',)
    list_editable = ('is_visible_on_main', 'is_visible', 'order',)
    search_fields = ('url', 'title')
    prepopulated_fields = {"url": ("title",)}
    #Тут втыкаем новое сео
    inlines = [seo_inline()]

    def get_actions(self, request):
        actions = super(AdvantageAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (delete_selected_item, 'delete_selected', u"Удалить выбранные преимущества")
        return actions


admin.site.register(Advantage, AdvantageAdmin)


class IndexPageAdmin(admin.ModelAdmin):
    #Тут втыкаем новое сео
    inlines = [seo_inline()]

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
                attrs={'cols': 80, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Содержимое страницы', label=u'Содержимое страницы', required=False)

        if db_field.name in ('seo_text',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Текст внизу на главной', label=u'Сео Текст', required=False)

        return super(IndexPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(IndexPage, IndexPageAdmin)