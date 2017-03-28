# -*- coding: utf-8 -*-

from constance import config
from django.shortcuts import render, get_object_or_404
from models import Announce
from main.views import simple_pagination
from flatpages.models import FlatPage

def announce_list(request=None):
    per_page = config.ANNOUNCES_PER_PAGE
    page_url = '/anonsy/'
    flatpages = FlatPage.objects.filter(url=page_url)
    if flatpages:
        flatpage = flatpages[0]

    breadcrumbs = [{"title": "Анонсы" }]
    items = simple_pagination(request, Announce.objects.filter(is_visible=True).order_by("-created_at"), per_page)
    context = {"list": items.object_list,
               "items": items }

    return render(request, "announce/list.html", locals())


def announce_detail(request, slug):
    item = get_object_or_404(Announce, slug=slug)
    breadcrumbs = [{"title": "Анонсы", "url": '/anonsy/' },
                   {"title": item.get_title()}
                   ]
    return render(request, "announce/detail.html", locals())