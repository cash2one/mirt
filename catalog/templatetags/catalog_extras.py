# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy

from catalog.models import Directory, Product, Brand, Promotion, ProductAccessory
from operator import itemgetter
from constance import config
from datetime import date
from django.db.models.query_utils import Q
from django import template
from django.db.models import Max, Min
import re

register = template.Library()


@register.inclusion_tag('templatetags/side_menu.html')
def catalog_side_menu(url=''):
    expand = []
    if url:
        for item in Directory.objects.get(slug=url).get_ancestors(include_self=True):
            if not item.is_leaf_node():
                expand.append(item.slug)
    
    nodes = Directory.object.filter(is_visible=True)
    return {'nodes': nodes, 'url': url, 'expand': expand}


@register.inclusion_tag('templatetags/side_menu_old.html')
def catalog_side_menu_old(url=''):
    expand = []
    if url:
        for item in Directory.objects.get(slug=url).get_ancestors(include_self=True):
            if not item.is_leaf_node():
                expand.append(item.slug)

    nodes = Directory.tree.filter(is_visible=True)
    return {'nodes': nodes, 'url': url, 'expand': expand}


@register.inclusion_tag('templatetags/side_colmenu.html')
def catalog_side_colmenu(url=''):
    nodes = Directory.objects.filter(is_visible=True, directory__isnull=True)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/side_colmenuinner.html')
def catalog_side_colmenuinner(url=''):
    nodes = Directory.objects.filter(is_visible=True, directory__isnull=True)
    return {'nodes': nodes, 'url': url}


@register.inclusion_tag('templatetags/side_subcolmenu.html')
def catalog_side_subcolmenu(id):
    nodes = Directory.objects.filter(is_visible=True, directory__id=id)
    return {'nodes': nodes}


@register.inclusion_tag('templatetags/side_2subcolmenu.html')
def catalog_sub2colmenu(id):
    nodes = Directory.objects.filter(is_visible=True, directory__id=id)
    return {'nodes': nodes}


@register.inclusion_tag('templatetags/side_2subcolmenuclass.html')
def catalog_sub2colmenuclass(id):
    nodes = Directory.objects.filter(is_visible=True, directory__id=id)
    return {'nodes': nodes}


@register.inclusion_tag('templatetags/side_2subcolmenuclasslili.html')
def catalog_sub2colmenulili(id):
    nodes = Directory.objects.filter(is_visible=True, directory__id=id)
    return {'nodes': nodes}


@register.inclusion_tag('catalog/tags/bottom_menu.html')
def catalog_bottom_menu(url=''):
    nodes = Directory.tree.filter(is_visible=True, show_in_bottom_menu=True)
    return {'nodes': nodes, 'url': url}


def get_first_found_digit(value):
    digit = re.search("(?P<digit>\d+)", value[0])
    if digit:
        value = digit.group()
    return value


def sort_values_x(values):
    if not all(x[1] for x in
               values):  # если порядок везде 0, сортируем по первой группе цифр, найденных в значении характеристики
        sorted_values = sorted(values, key=get_first_found_digit)
    else:
        sorted_values = sorted(values, key=itemgetter(1))  # сортируем по порядку
    values = list(x[0] for x in sorted_values)
    return values


# для слайдера c акциями
class ProductSet(object):
        def paginate(self, queryset):
            per_slide = 4
            some_len = queryset.count()
            some_range = some_len/per_slide + int(bool(some_len%per_slide))
            if some_range > 1:
                self.has_pages = True
            for n in range(0, some_range):
                self.pages.append(queryset[(per_slide*n):(per_slide*(n+1))])


        def __init__(self,name,products_queryset):
            self.taitle = name
            self.has_pages = False
            self.pages = []
            self.paginate(products_queryset)


# для слайдера c акциями
def get_products_by_promotion_type(type_promo):
    promotions = Promotion.objects.filter(Q(type=type_promo[0]) & Q(Q(start_at=None, finish_at=None) |
                                                                 Q(start_at__lte=date.today, finish_at=None) |
                                                                 Q(start_at=None, finish_at__gte=date.today) |
                                                                 Q(start_at__lte=date.today, finish_at__gte=date.today))
    )

    promotion_set = None

    if promotions:
        prod_list = []
        for pr in promotions:
            prod_list.append(pr.product.id)
        all_products = Product.objects.filter(pk__in=prod_list)
        promotion_set = ProductSet(type_promo[1], all_products)
    return promotion_set


# слайдер c акциями
@register.inclusion_tag('catalog/tags/products_promotion_slider.html')
def products_promotion_slider():
    promotion_sets = []
    for type in Promotion.PROMOTION_TYPE:
        promo_set = get_products_by_promotion_type(type)
        if promo_set:
            promotion_sets.append(promo_set)
    return {"product_sets": promotion_sets}


@register.inclusion_tag('catalog/tags/products_promotion_slider.html')
def products_similar_and_accessories_slider(product):
    product_sets = []

    # accessories = []
    # if product.directory.accessory:
    #     for dir in product.directory.accessory.all():
    #         accessories.append(dir.id)
    #
    # dir_accessories = []
    # if product.directory.dir_accessory:
    #     for dir in product.directory.dir_accessory.all():
    #         dir_accessories.append(dir.id)

    # acces_prod_extra_ids = ProductAccessory.objects.filter(product__id=product.id).values_list('accessory__id',flat=True)
    # products_accessories = Product.objects.filter(
    #     (Q(id__in=acces_prod_extra_ids) | Q(accessory__in=accessories) | Q(directory__in=dir_accessories)) & Q(is_visible=True))
    #
    # if products_accessories:
    #     product_sets.append(ProductSet("Аксессуары",products_accessories))

    simillar_products = product.get_simillar()
    if simillar_products:
        product_sets.append(ProductSet("Рекомендуемые товары", simillar_products))

    return {"product_sets": product_sets}


@register.inclusion_tag('catalog/tags/products_promotion_slider_old.html')
def products_similar_and_accessories_slider_old(product):
    product_sets = []

    # accessories = []
    # if product.directory.accessory:
    #     for dir in product.directory.accessory.all():
    #         accessories.append(dir.id)
    #
    # dir_accessories = []
    # if product.directory.dir_accessory:
    #     for dir in product.directory.dir_accessory.all():
    #         dir_accessories.append(dir.id)

    # acces_prod_extra_ids = ProductAccessory.objects.filter(product__id=product.id).values_list('accessory__id',flat=True)
    # products_accessories = Product.objects.filter(
    #     (Q(id__in=acces_prod_extra_ids) | Q(accessory__in=accessories) | Q(directory__in=dir_accessories)) & Q(is_visible=True))
    #
    # if products_accessories:
    #     product_sets.append(ProductSet("Аксессуары",products_accessories))

    simillar_products = product.get_simillar()
    if simillar_products:
        product_sets.append(ProductSet("Рекомендуемые товары", simillar_products))

    return {"product_sets": product_sets}


# @register.inclusion_tag('catalog/filter_widget/filter_form.html', takes_context=True)
# def catalog_filter(context):
#     filter_widget = context.get("filter_widget", None)
#     return {"filter_widget": filter_widget}


# @register.inclusion_tag('catalog/tags/product_set.html', takes_context=True)
# def similar_products(context):
#     product_set = None
#     taitle = "Аналоги"
#     product = context.get("product", None)
#
#     if product:
#         products = product.get_simillar()
#         if products:
#             class set(object):
#                 pass
#
#             product_set = set()
#             product_set.preview_products = products[0:4]
#             product_set.preview_products_count = products.count()
#             product_set.get_absolute_url = "/analogi/%s/" % product.id
#     return {"product_set": product_set, "taitle": taitle}


class AccessoryGroup(object):
    def __init__(self):
        pass


#TODO: аксессуары и аналогичные товары
@register.inclusion_tag('catalog/tags/accessories_and_similar_products.html')
def accessories_and_similar_products(product_id):
    # try:
    #     product = Product.objects.get(id=product_id)
    #     directory = Product.directory
    # except:
    #     return {'accessories': [], 'directories': []}
    # accessories = []
    # if directory.accessory:
    #     for dir in directory.accessory.all():
    #         accessories.append(dir.id)
    #
    # products = []
    # dir_accessories = []
    # if directory.dir_accessory:
    #     for dir in directory.dir_accessory.all():
    #         dir_accessories.append(dir.id)
    # acces_prod_extra_ids = ProductAccessory.objects.filter(product__id=product_id).values_list('accessory__id',flat=True)
    #
    # products = Product.objects.filter(
    #     (Q(id__in=acces_prod_extra_ids) | Q(accessory__in=accessories) | Q(directory__in=dir_accessories)) & Q(is_visible=True))[:4]
    #
    # directories = Directory.objects.filter(Q(id__in=dir_accessories) | Q(
    #     id__in=Product.objects.filter(accessory__in=accessories, is_visible=True).values('directory__id')))
    #
    # for directory in directories:
    #     directory.preview_products = []
    #     list_len = 0
    #     for product in products:
    #         if product.directory == directory and (list_len < 5):
    #             list_len += 1
    #             directory.preview_products.append(product)
    #             directory.preview_products_count = list_len


    return {'acc_groups': [], 'similar_products_link': "#"}


# товары на главной
@register.inclusion_tag('catalog/tags/product_set.html', takes_context=True)
def index_products(context):
    product_set = None
    taitle = "Хиты продаж"

    products = Product.objects.filter(is_visible=True, show_on_main=True)
    if products:
        class set(object):
            pass
        limit = 4
        try:
            limit = int(config.PRODUCTS_ON_MAIN)
        except:
            limit = 4

        product_set = set()
        product_set.preview_products = products[0:limit]
        product_set.preview_products_count = products.count()
        product_set.get_absolute_url = reverse_lazy("catalog:index-products")
    return {"product_set": product_set, "taitle": taitle}


@register.inclusion_tag('catalog/tags/mainpage_news.html')
def catalog_novinki():
    nodes = Promotion.objects.filter(type='new')[0:4]
    return {'nodes': nodes}


@register.inclusion_tag('catalog/tags/mainpage_sale.html')
def catalog_superprice():
    nodes = Promotion.objects.filter(type='sale')[0:4]
    return {'nodes': nodes}


@register.inclusion_tag('catalog/tags/mainpage_special.html')
def catalog_spest():
    nodes = Promotion.objects.filter(type='special')[0:4]
    return {'nodes': nodes}