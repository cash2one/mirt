# -*- coding: utf-8 -*-
from constance import config

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from main.views import simple_pagination, get_products_per_page
from quick_links.models import QuickLink, QuickDirectoryLink, QuickProductLink,\
    QuickBrandLink, QuickGroupLink, ProductFromGroup
from catalog.models import Product
from django.template.loader import render_to_string
import json


def link_detail(request, slug):
    # TODO: создание контейнера для вывода товаров
    # https://simplemedia.atlassian.net/browse/MEZON-69
    link = None
    active = None

    if not link:
        slug = slug.replace('/', '')
        link = get_object_or_404(QuickLink, slug=slug, is_visible=True)

    if link:
        active = link.id

    dirs = QuickDirectoryLink.objects.filter(quick_link=link, directory__is_visible=True).order_by('order').values_list("directory__pk", flat=True)

    brands = QuickBrandLink.objects.filter(quick_link=link,).order_by('order').values_list("brand__pk", flat=True)

    groups = QuickGroupLink.objects.filter(quick_link=link).order_by('order').values_list('group_id', flat=True)
    group_Products = ProductFromGroup.objects.filter(group__id__in=groups, product__is_visible=True).values_list("product__pk", flat=True)

    prods = QuickProductLink.objects.filter(quick_link=link, product__is_visible=True).values_list("product__pk", flat=True)

    all_pk_products = Product.objects.filter(Q(pk__in=prods) | Q(pk__in=group_Products) | Q(brand__pk__in=brands) | Q(directory__pk__in=dirs))
    all_pk_products = all_pk_products.filter(is_visible=True)

    sort_is = ""
    sort_qs = ""

    price_desc = False
    if request.GET.has_key("sort"):
        sort_is = request.GET['sort']
        sort_qs = u"sort=%s" % sort_is
        if request.GET["sort"] == "price_desc":
            price_desc = True

    all_pk_products = sorted(all_pk_products, key=lambda item: item.price, reverse=price_desc)


    products = []
    products_list = []
    if all_pk_products:
        products = simple_pagination(request, all_pk_products, config.CATALOG_PER_PAGE)

    qs = ""
    per_page_qs = ""
    per_page = False

    if products:
        if sort_is:
            per_page_qs += u"&"
        per_page_qs += qs

    if per_page:
        if sort_is:
            qs += u"&"
        qs += u"per_page=%s" % per_page

    context = {
        "link": link,
        "breadcrumbs": link.get_breadcrumbs(),
        "items": products,
        "qs": qs,
        "per_page": per_page,
        "per_page_qs": per_page_qs,
        "sort_qs": sort_qs,
        "sort_is": sort_is
    }

    return render(request, 'quick_links/detail.html', context)
