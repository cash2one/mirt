# -*- coding: utf-8 -*-
from django.utils.functional import curry

from catalog.models import Directory, Product, Promotion, Brand, Image, FeatureGroup, FeatureValue, Feature, \
    FeatureValueGroup, Accessories, ProductAccessory, WebStockProduct, OneCstock, WebStock
from django.contrib import admin, messages

from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django import forms

from tinymce.widgets import TinyMCE
from feincms.admin import tree_editor
from quick_links.models import ProductGroup, ProductFromGroup

from datetime import datetime

from simpleseo.admin import seo_inline

from datetime import date
from django.contrib.admin.actions import delete_selected as delete_selected_item

class ProductAccessoryInline(admin.TabularInline):
    model = ProductAccessory
    fk_name = "product"
    extra = 0
    raw_id_fields = ('accessory',)
    autocomplete_lookup_fields = {
        'fk': ['accessory',],
    }


class ProductStockInline(admin.TabularInline):
    model = WebStockProduct
    fk_name = "product"
    extra = 0
    raw_id_fields = ('webstock',)
    autocomplete_lookup_fields = {
        'fk': ['webstock',],
    }


class OneCStockInline(admin.TabularInline):
    model = OneCstock
    fk_name = "webstock"
    extra = 0


class WebStockAdmin(admin.ModelAdmin):
    inlines = [OneCStockInline,]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('text',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'', label=u'Текстовое описание склада', required=False)

        return super(WebStockAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(WebStock, WebStockAdmin)


class FeatureGroupInline(admin.TabularInline):
    model = FeatureGroup
    extra = 0
    raw_id_fields = ('directory',)
    autocomplete_lookup_fields = {
        'fk': ['directory',],
    }

class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 0
    raw_id_fields = ('feature',)
    autocomplete_lookup_fields = {
        'fk': ['feature',],
    }

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('feature', 'value')}
        ),
    )

    def get_formset(self, request, obj=None, **kwargs):
        return super(FeatureValueInline, self).get_formset(request, obj=obj,
                                                           formfield_callback=curry(self.formfield_for_dbfield,
                                                                                    request=request, obj=obj)
        )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if 'obj' in kwargs and db_field.name != 'feature':
            del kwargs['obj']
        return super(FeatureValueInline, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, field, request, **kwargs):
        if field.name == 'feature':
            if 'obj' in kwargs and kwargs['obj']:
                directories = kwargs['obj'].directory.get_ancestors(include_self=True)
                kwargs['queryset'] = Feature.objects.filter(group__directory__in=directories).distinct()
            del kwargs['obj']
        return super(FeatureValueInline, self).formfield_for_foreignkey(field, request, **kwargs)

#Пока не палим
class FeatureValueGroupInline(admin.TabularInline):
    model = FeatureValueGroup
    extra = 0
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'regexp', 'order')}
        ),
    )

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_directory', 'group', 'widget_type', 'order', 'is_primary', 'is_filter')
    list_editable = ('widget_type', 'order', 'is_primary', 'is_filter')
    list_filter = ('widget_type', 'group', 'is_primary', 'is_filter', 'group__directory')
    #inlines = [FeatureValueGroupInline]
    raw_id_fields = ('group',)
    autocomplete_lookup_fields = {
        'fk': ['group',],
    }
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('group', 'name', 'widget_type', 'order', 'is_primary'), }
        ),
    )

    def get_directory(self, obj):
        return obj.group.directory.name

    get_directory.short_description = u"Раздел каталога"
    get_directory.admin_order_field = 'group__directory__name'

admin.site.register(Feature, FeatureAdmin)


class FeatureGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'directory',)
    list_filter = ('directory',)
    search_fields = ('name',)
    raw_id_fields = ('directory',)
    autocomplete_lookup_fields = {
        'fk': ['directory',],
    }

admin.site.register(FeatureGroup, FeatureGroupAdmin)


class DirectoryAdmin(tree_editor.TreeEditor):
    list_display = ('name', 'is_visible','show_in_bottom_menu', 'order',)
    list_editable = ('is_visible','show_in_bottom_menu', 'order')
    prepopulated_fields = {"slug": ("name",)}

    raw_id_fields = ('accessory','dir_accessory',)
    autocomplete_lookup_fields = {
        'm2m': ['accessory','dir_accessory',],
    }
    def _actions_column(self, page):
        actions = []
        actions.insert(0, u'<a href="/admin/catalog/product/?directory__id__exact=%s" title="перейти к списку товаров раздела">К списку товаров</a>' % page.pk )
        return actions
    _actions_column.short_description = u'Перейти'

    def get_actions(self, request):
        actions = super(DirectoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (delete_selected_item, 'delete_selected', u"Удалить выбранные страницы сайта")
        return actions

    #search_fields = ('name',)
    #list_filter = ('directory', 'is_visible')

    inlines = [seo_inline()]

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'singular_name', 'slug', 'directory', 'is_visible', 'show_in_bottom_menu', 'order',
                'top_description', 'bottom_description',)}
        ),
        (u'Акссесуары', {
            'classes': ('wide',),
            'fields': ('accessory', 'dir_accessory')}
        ),
        (u'1С', {
            'classes': ('collapse',),
            'fields': ('onec',)}
        ),
        # (u'Шаблон метаданных продукта', {
        #     'classes': ('collapse',),
        #     'fields': ('seo_title', 'seo_description', 'seo_keywords')}
        # ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('top_description',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Описание, отображаемое в верхней части страницы', label=u'Верхнее описание', required=False)

        if db_field.name in ('bottom_description',):
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 10},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Описание, отображаемое в нижней части страницы', label=u'Нижнее описание', required=False)

        return super(DirectoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        queryset = self.queryset(request)
        try:
            object_id = int(object_id)
            obj = queryset.get(pk=object_id)
        except ValueError:
            obj = None

        if db_field.name == 'directory' and obj:
            kwargs['queryset'] = Directory.objects.exclude(id__in=obj.get_descendants(include_self=True))
        return super(DirectoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        #     if db_field.name in ('extra_directories', 'dir_accessory'):
        #         kwargs['empty_label'] = None
            return super(DirectoryAdmin, self).formfield_for_manytomany(db_field, **kwargs)


admin.site.register(Directory, DirectoryAdmin)


class ImageInline(generic.GenericStackedInline):
    model = Image
    extra = 0


def create_new_group(modeladmin, request, queryset):

    name = u"Новая группа [ %s ]" % datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    new_group = ProductGroup(name=name)
    new_group.save()

    for q in queryset:
        dur = ProductFromGroup(product = q, group = new_group )
        dur.save()

    message_bit = name
    # modeladmin.message_user(request, u"Создана группа - %s, %s" % (message_bit, link) ,extra_tags='safe')
    messages.success(request, u"Создана новая группа товаров - %s" % message_bit)
create_new_group.short_description = u'Создать группу для быстрых ссылок'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'directory', 'brand', 'price', 'is_visible', 'show_on_main',)
    list_editable = ('directory', 'price', 'is_visible', 'show_on_main',)
    list_filter = ('directory', 'brand', 'is_visible','show_on_main',)
    search_fields = ('name', 'directory__name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductAccessoryInline, ImageInline,FeatureValueInline,ProductStockInline, seo_inline()]
    actions = [create_new_group]
    raw_id_fields = ('accessory',)
    autocomplete_lookup_fields = {
        'fk': ['accessory',],
    }


    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'slug', 'directory', 'brand', 'price', 'is_visible','show_on_main', 'accessory')}
        ),
        (u'Описание товара', {
            'classes': ('collapse',),
            'fields': ('short_description', 'description')}
        ),
        (u'1С', {
            'classes': ('collapse',),
            'fields': ('articul', 'onec','onecdir',)}
        ),

    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'short_description':
            return forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), label=u'Краткое описание товара',
                                   required=False)

        if db_field.name == 'description':
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ), help_text=u'Описание наимменования товара', label=u'Описание', required=False)


        return super(ProductAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return tuple()
        return self.readonly_fields


    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(ProductAdmin, self).response_add(request, obj, post_url_continue)


admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',)}
        ),
    )

admin.site.register(Brand, BrandAdmin)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('type', 'get_product', 'get_directory', 'start_at', 'finish_at', 'is_active')
    list_filter = ('type', 'product__directory','product__name')
    list_editable = ('start_at', 'finish_at')
    raw_id_fields = ('product',)

    def get_product(self, obj):
        ref = u'/admin/catalog/product/%s/' % obj.product.id
        return u'<a href="%s">%s</a>' % (ref,obj.product.name)
    get_product.admin_order_field = 'product'
    get_product.allow_tags = True
    get_product.short_description = u'Товар'

    def get_directory(self, obj):
        return obj.product.directory.name

    get_directory.short_description = u"Раздел каталога"
    get_directory.admin_order_field = 'product__directory'

    def is_active(self, obj):
        obj.is_active = u"Не активна"
        if (not obj.finish_at) or obj.finish_at > date.today():
            obj.is_active = u"Активна"
        return obj.is_active

    is_active.short_description = u"Статус"

admin.site.register(Promotion, PromotionAdmin)


class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',)}
        ),
    )

    actions = ['delete_only_directory_accessories']

    def get_actions(self, request):
        actions = super(AccessoryAdmin, self).get_actions(request)
        try:
            del actions['delete_selected']
        except:
            pass
        return actions

    def delete_only_directory_accessories(self, request, queryset):
        for obj in queryset:
            products = Product.objects.filter(accessory=obj)
            for product in products:
                product.accessory = None
                product.save()
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 directory accessories entry was"
        else:
            message_bit = "%s directory accessories entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    delete_only_directory_accessories.short_description = u'Удалить только раздел акессуаров'


admin.site.register(Accessories, AccessoryAdmin)
