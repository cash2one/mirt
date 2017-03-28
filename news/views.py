# -*- coding: utf-8 -*-

from constance import config
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from main.views import simple_pagination
from models import News
from flatpages.models import FlatPage


def news_list(request=None):
    per_page = config.NEWS_PER_PAGE
    page_url = '/novosti/'
    flatpages = FlatPage.objects.filter(url=page_url)
    if flatpages:
        flatpage = flatpages[0]
    breadcrumbs = [{"title": "Новости" }]
    items = simple_pagination(request, News.objects.filter(is_visible=True).order_by("-created_at"), per_page)
    context = {"list": items.object_list,
               "items": items}

    return render(request, "news/list.html", locals())


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug)

    breadcrumbs = [{"title": "Новости","url":'/novosti/' },
                   {"title": item.title }
                   ]
    return render(request, "news/detail.html", locals())

