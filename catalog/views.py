# -*- coding: utf-8 -*-
from constance import config
from django.core.urlresolvers import reverse_lazy
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
import json, re
from django.template.loader import render_to_string
from catalog.models import Directory, Product, Image, Promotion, Brand, Feature, FeatureValue, WebStockProduct, WebStock
from main.views import simple_pagination, get_products_per_page
from catalog.filter_widget import FilterWidget
import random
from datetime import date


def filter_by_features(request, products, filter_widget=None):
    directory_id_list = products.values_list("directory__id", flat=True)
    features = list(Feature.objects.filter(is_filter=True, group__directory__id__in=directory_id_list))
    products_ids = products.values_list("id", flat=True)

    param = None
    if request.method == 'GET':
        param = request.GET
    bypass_list_fader = []

    #отображение фильтра
    for f in features:
        name = '%s_%s' % (f.widget_type, f.id)
        featuresvalues = FeatureValue.objects.filter(feature__id=f.id, product__id__in=products_ids).order_by('value')
        if f.widget_type == 'fader_double':
            if featuresvalues:
                featuresvalues = list(featuresvalues)
                minvalue = featuresvalues[0].value
                current_min = minvalue
                maxvalue = featuresvalues[-1].value
                current_max = maxvalue
                if name+' min' in param:
                    try:
                        current_min = int(param.get(name+' min').replace(' ',''))
                    except:
                        pass
                if name+' max' in param:
                    try:
                        current_max = int(param.get(name+' max').replace(' ',''))
                    except:
                        pass

                fader_kwargs = {"name": name,
                                "type": "fader_double",
                                "label": f.name,
                                "order": f.order,
                                "min": minvalue,
                                "max": maxvalue,
                                "current_min":current_min,
                                "current_max":current_max}
                do_filter = filter_widget.update_feature(**fader_kwargs)
                if not do_filter:
                    bypass_list_fader.append(name+' min')
                    bypass_list_fader.append(name+' max')
        elif f.widget_type == 'select_box':
            if featuresvalues:
                selected_list = []
                if name in param:
                    selected_list = param.getlist(name)
                #Создаём список вариантов выбора
                list_for_out = []
                used_value = []
                for fv in list(featuresvalues):
                    if fv.value not in used_value:
                        used_value.append(fv.value)
                        list_for_out.append((fv.id,fv.value))
                fader_kwargs = { "name":name,
                                 "type":f.widget_type,
                                 "label":f.name,
                                 "order":f.order,
                                 "with_labels":True,  # нада добаить этот параметр, чтобы
                                 "values":list_for_out,  # Вот тут важен порядок!
                                 "selected_values":map(long, selected_list, )}
                filter_widget.update_feature(**fader_kwargs)

        elif f.widget_type == 'checkbox':
            selected = False
            if name in param:
                selected = True
            fader_kwargs = { "name":name,
                             "type":f.widget_type,
                             "label":f.name,
                             "order":f.order,
                             "checked":selected}
            filter_widget.update_feature(**fader_kwargs)
    if param:
        for parametr in param:
            if parametr not in bypass_list_fader:
                if parametr.startswith('checkbox_'):
                    feature_id = None
                    try:
                        feature_id = long(parametr[9:])
                    except:
                        pass
                    if feature_id:
                        products_ids = FeatureValue.objects.filter(feature__id=feature_id, product__id__in=products_ids).values_list('product__id',flat=True)

                elif parametr.startswith('select_box_'):
                    values = []
                    try:
                        for fvid in param.getlist(parametr):
                            try:
                                values.append(long(fvid))
                            except:
                                pass
                    except:
                        pass

                    if values:

                        full_values = FeatureValue.objects.filter(id__in = values).values_list('value', flat=True)
                        products_ids = FeatureValue.objects.filter(product__id__in=products_ids, value__in = full_values).values_list('product__id',flat=True)

                elif parametr.startswith('fader_double'):

                    pl = parametr.split(' ')
                    feature_id = None
                    try:
                        feature_id = long(pl[0][13:])
                    except:
                        pass
                    if feature_id:
                        if 'max' == pl[1]:
                            try:
                                products_ids = FeatureValue.objects.filter(feature__id=feature_id, product__id__in=products_ids,value__lte=int(param.get(parametr).replace(' ',''))).values_list('product__id',flat=True)
                            except:
                                pass
                        if 'min' == pl[1]:
                            try:
                                products_ids = FeatureValue.objects.filter(feature__id=feature_id, product__id__in=products_ids,value__gte=int(param.get(parametr).replace(' ',''))).values_list('product__id',flat=True)
                            except:
                                pass

    brands = list(products.order_by('brand__name').values_list('brand__id','brand__name'))

    list_for_out = []
    selected_list = []

    for bid, bnam in brands:
        if bid:
            if (bid, bnam) not in list_for_out:
                list_for_out.append((bid, bnam))

    if param.has_key('brand'):
        selected_list = param.getlist('brand')

    if len(list_for_out) > 0:

        filter_widget.update_feature(name=u'brand',
                                     type='select_box',
                                     label=u'Брэнд',
                                     order=99,
                                     with_labels=True,  # нада добаить этот параметр, чтобы
                                     values=list_for_out,  # Вот тут важен порядок!
                                     selected_values=map(long, selected_list, )
        )

    prices = list(products.order_by('price').values_list('price',flat=True))
    minvalue = int(prices[0])
    maxvalue = int(prices[-1])
    selected_min_price = minvalue
    selected_max_price = maxvalue

    price_kwargs = {"name": "price",
                  "type": "fader_double",
                  "label": u"Цена",
                  "order": 100,
                  "min": minvalue,
                  "max": maxvalue}

    if param.has_key('price min'):
        try:
            selected_min_price = int(param.get('price min').replace(" ",""))
            price_kwargs.update({"current_min": selected_min_price})
        except:
            pass

    if param.has_key('price max'):
        try:
            selected_max_price = int(param.get('price max').replace(" ",""))
            price_kwargs.update({"current_max": selected_max_price })
        except:
            pass

    filter_widget.update_feature(**price_kwargs)

    if products_ids:
        if selected_list:
            products = products.filter(id__in=products_ids,price__gte=selected_min_price,price__lte=selected_max_price,brand__id__in=selected_list)
        else:
            products = products.filter(id__in=products_ids,price__gte=selected_min_price,price__lte=selected_max_price)
    else:
        products = []
    return products, filter_widget


def filter_by_order(request, products):
    #get a data for ordering
    try:
        sort = request.POST['sort']
    except:
        try:
            sort = request.GET['sort']
        except:
            sort = None
    if sort == 'price':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    return products, sort


# из url вида /some/url/here/ берем "here" - т.е. последний слаг
def get_exact_directory(string):
    directories_slug = re.split('/', string)
    directory = None
    for slug in directories_slug[:-1]:
        directory = Directory.objects.get(directory=directory, slug=slug)
    return directory


# раздел
def directory_detail_view(request, slug):
    # TODO: создание контейнера для вывода товаров
    # https://simplemedia.atlassian.net/browse/MEZON-69
    try:
        directory = get_exact_directory(slug)
    except Directory.DoesNotExist:
        # ***
        # костыль, йопт!  разбиираем урл на урл раздела и слаг товара
        # например /razdel/eshe_razdel/tovar/ =>
        #   slug : /razdel/eshe_razdel/
        #   item :                     tovar
        # ***
        grups = re.search("^(?P<slug>[\w/-]+)/(?P<item>[-\w]+)/$", slug)
        if grups:
            slug = grups.group("slug") + "/"
            item = grups.group("item")
            return product_detail_view(request, slug, item)
        else:
            raise Http404

    context = {
        'directory': directory,
        'breadcrumbs': directory.get_breadcrumbs(), }

    products = Product.objects.filter(directory=directory, is_visible=True)

    qs = ""
    filter_qs = ""
    per_page_qs = ""
    sort_is = False
    filter_widget = None

    subdirectories = []

    filter_found = None

    per_page = False

    if products:

        filter_widget = FilterWidget(directory.get_absolute_url())
        products, sort_is = filter_by_order(request, products)
        products, filter_widget = filter_by_features(request, products, filter_widget)
        if products:
            filter_found = products.count()
        else:
            filter_found = 0
        products, per_page = get_products_per_page(request, products)

    else:
        products = []
        for dirr in directory.get_children():
            dir_ids = dirr.get_descendants(True)
            dir_prods = Product.objects.filter(directory__id__in=dir_ids, is_visible=True)
            dir_prod_pop = Product.objects.filter(directory__id__in=dir_ids, is_visible=True)
            if dir_prod_pop.count()>4:
                dirr.preview_products = random.sample(dir_prod_pop, 4)
                dirr.preview_products_count = dir_prods.count
            else:
                dirr.preview_products = dir_prod_pop
                dirr.preview_products_count = dir_prod_pop.count()
            subdirectories.append(dirr)

    if sort_is:
        qs = u"sort=%s" % sort_is

    if products:
        if sort_is:
            per_page_qs += u"&"
        per_page_qs += qs

    if per_page:
        if sort_is:
            qs += u"&"
        qs += u"per_page=%s" % per_page

    if filter_widget:
        for feature in filter_widget.get_features():
            if feature.widget.query_string:
                filter_qs += ("&%s" % feature.widget.query_string)

    context.update({"items": products,
                    "qs": qs,
                    "filter_qs": filter_qs,
                    "sort_is": sort_is,
                    "per_page": per_page,
                    "per_page_qs": per_page_qs,
                    "filter_widget": filter_widget,
                    "subdirectories": subdirectories,
                    "filter_found": filter_found,
    })

    return render(request, 'catalog/directory_detail.html', context)


# все товары, которые крепятся на главную
def index_products(request):
    context = {
        'breadcrumbs': [{"title": "Хиты продаж"}], }

    products = Product.objects.filter(is_visible=True, show_on_main=True)

    qs = ""
    filter_qs = ""
    per_page_qs = ""
    sort_is = False
    filter_widget = None

    filter_found = None

    per_page = False

    if sort_is:
        qs = u"sort=%s" % sort_is

    if products:
        filter_widget = FilterWidget(reverse_lazy("catalog:index-products"))
        products, sort_is = filter_by_order(request, products)
        products, filter_widget = filter_by_features(request, products, filter_widget)
        products, per_page = get_products_per_page(request, products)

        if sort_is:
            qs = u"sort=%s" % sort_is

        if products:
            if sort_is:
                per_page_qs += u"&"
            per_page_qs += qs

        if per_page:
            if sort_is:
                qs += u"&"
            qs += u"per_page=%s" % per_page

        if filter_widget:
            for feature in filter_widget.get_features():
                if feature.widget.query_string:
                    filter_qs += ("&%s" % feature.widget.query_string)

    context.update({"items": products,
                    "qs": qs,
                    "filter_qs": filter_qs,
                    "sort_is": sort_is,
                    "per_page": per_page,
                    "per_page_qs": per_page_qs,
                    "filter_widget": filter_widget,
                    "filter_found": filter_found,
    })

    return render(request, 'catalog/directory_detail.html', context)


def render_marker_data(request, id, product_id):
    data = {"success": False}
    stocks = WebStock.objects.filter(id=id)
    if stocks:
        webstock = stocks[0]
        product_count = WebStockProduct.objects.filter(webstock=webstock, product__id=product_id)[0].count
        html = render_to_string("catalog/tags/marker_data.html", {"marker": webstock, "product_count": product_count })
        data.update({"success": True, "html": html})

    return HttpResponse(json.dumps(data), mimetype="application/json")

# сам товар
def product_detail_view(request, slug, item):
    try:
        product = Product.objects.filter(Q(slug=item, is_visible=True) & (Q(directory=get_exact_directory(slug))))[0]
    except:
        raise Http404

    images = product.get_secondary_images()

    use_slider = False
    images_per_set = 3
    images_count = images.count()

    if images_count > images_per_set:
        sets = []

        use_slider = True

        for i in xrange(0, images_count, images_per_set):
            sets.append(images[i:i+images_per_set])

        images = sets

    stocks, map_data = product.get_stocks_data()

    context = {
        'product': product,
        'breadcrumbs': product.get_breadcrumbs(),
        'images': images,
        'use_slider': use_slider,
        'stocks': stocks,
        'map_data': map_data
    }

    return render(request, 'catalog/product_detail.html', context)


# товары по акции
def list_promo_products(request, type_promo):
    # type_promo = Promotion.objects.filter(type=type_promo)
    # if not type_promo:
    #     raise Http404

    promotions = Promotion.objects.filter(
        Q(type=type_promo) & Q(
            Q(start_at=None, finish_at=None) |
            Q(start_at__lte=date.today, finish_at=None) |
            Q(start_at=None, finish_at__gte=date.today) |
            Q(start_at__lte=date.today, finish_at__gte=date.today)
        )
    )

    prod_list = []
    for pr in promotions:
        prod_list.append(pr.product.id)

    products = Product.objects.filter(pk__in=prod_list)

    sort_is = ""
    qs = ""

    if products:
        products, sort_is = filter_by_order(request, products)
        products = simple_pagination(request, products, 16)
    else:
        products = []

    if sort_is:
        qs = u"sort=%s" % sort_is

    context = {
        'promotion': type_promo[0],
        'breadcrumbs': type_promo[0].get_breadcrumbs(),
        "items": products,
        "qs": qs,
        "sort_is": sort_is
    }

    return render(request, 'catalog/promotion_detail.html', context)


# схожие по цене товары
def similar_products(request, id):
    product = get_object_or_404(Product, id=id, is_visible=True)
    products = product.get_simillar()
    sort_is = ""
    qs = ""

    if products:
        products, sort_is = filter_by_order(request, products)
        products = simple_pagination(request, products, 16)
    else:
        products = []

    if sort_is:
        qs = u"sort=%s" % sort_is

    breadcrumbs = product.get_breadcrumbs()
    breadcrumbs.append({"title": "аналоги"})
    context = {
        'breadcrumbs': breadcrumbs,
        "product": product,
        "items": products,
        "qs": qs,
        "sort_is": sort_is
    }

    return render(request, 'catalog/simillar_products.html', context)
