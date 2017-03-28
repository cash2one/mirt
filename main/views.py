# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Product, Directory
from flatpages.models import FlatPage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from constance import config
from news.models import News
from quick_links.models import QuickLink


def change_theme(request):
    if request.GET.has_key("theme"):
        theme = request.GET.get("theme")
        request.session.update({ "theme":theme })
    url = "/"
    try:
        url = request.META.get("HTTP_REFERER")
    except:
        pass
    return HttpResponseRedirect(url)


def disable_under_development_banner(request):
    if request.session:
        request.session["under_development_dismissed"] = True
    url = "/"
    try:
        url = request.META.get("HTTP_REFERER")
    except:
        pass

    return HttpResponseRedirect(url)


def sitemap_gen(request):
    host = Site.objects.get_current().domain
    flatpages = FlatPage.objects.filter(is_visible=True)
    news = News.objects.filter(is_visible=True)
    products = Product.objects.filter(is_visible=True)
    directory = Directory.objects.filter(is_visible=True)
    ql = QuickLink.objects.filter(is_visible=True)

    return render_to_response('sitemap.html', locals(), context_instance=RequestContext(request),
                              mimetype="application/xhtml+xml")


def simple_pagination(request, items, per_page=4):
    paginator = Paginator(items, per_page)

    try:
        page = int(request.GET['page'])
    except:
        page = 1

    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)

    #to display a range of 6 page
    if items_list.number < 4:
        if paginator.num_pages >= 5:
            items_list.range_page = paginator.page_range[0:5]
        else:
            items_list.range_page = paginator.page_range[0:paginator.num_pages]
    elif (items_list.number + 2) > paginator.num_pages:
        items_list.range_page = paginator.page_range[paginator.num_pages - 5:paginator.num_pages]
    else:
        items_list.range_page = paginator.page_range[items_list.number - 3:items_list.number + 2]

    return items_list


def get_products_per_page(request,products):
    per_page = config.CATALOG_PER_PAGE
    if request.GET.get("per_page"):
        per_page = request.GET.get("per_page")
    else:
        if request.POST.get("per_page"):
            per_page = request.POST.get("per_page")
    if per_page == "show_all":
        products = simple_pagination(request, products, products.count())
    else:
        products = simple_pagination(request, products, per_page)
    return products, per_page