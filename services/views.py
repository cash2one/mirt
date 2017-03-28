# -*- coding: utf-8 -*-
from models import Service
from constance import config
from django.shortcuts import render, get_object_or_404

# def services_list(request):
#     items = Service.objects.filter(is_visible=True, parent=None)
#     context = {"list": items }
#     return context


def service_detail(request, slug):
    item = get_object_or_404(Service, url=slug)

    # breadcrumbs = [{"title": "Услуги","url":'/uslugi/'},
    #                {"title": item.title }
    #                ]
    breadcrumbs = item.get_breadcrumbs()

    return render(request, "services/detail.html", locals())