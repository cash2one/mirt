# -*- coding: utf-8 -*-

import json
from django.contrib import messages
from catalog.models import Product
from message.models import Mail
from order.cart import ShoppingCart
from order.forms import OrderForm
from order.models import Order, OrderItem, OrderStatus, CartItem
from constance import config
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.validators import email_re
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.template.loader import render_to_string


def get_email_list(var):
    addresses = var.replace(' ', '').split(',')
    valid_emails = []
    for email in addresses:
        if bool(email_re.match(email)):
            valid_emails.append(email)
    return valid_emails


def customer_email(request, order):
    context = {
        'order':order,
        }

    if order.email:
        email_list = get_email_list(order.email)
        try:
            subject = Mail.objects.get(type='customer_email').subject
            html_content = Template(Mail.objects.get(type='customer_email').mail).render(Context(context))
            msg = EmailMessage(subject, html_content, config.ORDER_FROM_EMAIL, email_list)
            msg.content_subtype = "html"
            msg.send()
        except Exception, e:
            text = 'Ошибка %s'%e
            subject = 'покупка'
            html_content = render_to_string('text.html',{'context': text})
            msg = EmailMessage(subject, html_content, config.ORDER_FROM_EMAIL, email_list)
            msg.content_subtype = "html"
            msg.send()


def seller_email(request, order):
    email_list = get_email_list(config.ORDER_TO_EMAIL)
    try:
        context = {
            'order':order,
            }

        subject = Mail.objects.get(type='seller_email').subject
        html_content = Template(Mail.objects.get(type='seller_email').mail).render(Context(context))
        msg = EmailMessage(subject, html_content, config.ORDER_FROM_EMAIL, email_list)
        msg.content_subtype = "html"
        msg.send()
    except Exception, e:
            text = 'Ошибка %s'%e
            subject = 'покупка'
            html_content = render_to_string('text.html',{'context': text})
            msg = EmailMessage(subject, html_content, config.ORDER_FROM_EMAIL, email_list)
            msg.content_subtype = "html"
            msg.send()


def get_cart(request):
    return render(request, 'order/cart.html', {'cart': ShoppingCart(request)})


def add_to_cart(request, product_id, quantity=1):
    back_link = "/"
    if request.META:
        back_link = request.META.get("HTTP_REFERER", "/")

    product = Product.objects.get(id=product_id)
    cart = ShoppingCart(request)

    if 'quantity' in request.POST:
        quantity = abs(int(request.POST.get('quantity')))
    messages.success(request, request.message_after_adding_the_goods_into_the_basket)

    for item in cart:
        if item.product == product:
            cart.update(item.id, item.quantity + quantity)
            return HttpResponseRedirect(back_link)

    item = cart.add(product, product.price, quantity)
    return HttpResponseRedirect(back_link)


def remove_from_cart(request, item_id):
    cart = ShoppingCart(request)
    cart.remove(item_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_cart(request):
    cart = ShoppingCart(request)
    cart.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_cart(request, item_id, quantity):
    cart = ShoppingCart(request)
    cart.update(item_id, quantity, True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check_cart(cart):
    mes = False
    for item in cart:
        if item.product:
            if item.price != item.product.price:
                item.price = item.product.price
                mes = True
        else:
            item.price = 0
            mes = True
        item.save()
    return mes

def checkout(request):
    cart = ShoppingCart(request)
    form = False

    breadcrumbs = [{"title": "Корзина"}]

    if request.GET.has_key("continue"):
        form = OrderForm()
        if check_cart(cart):
            try:
                messages.success(request, request.message_cart_changed)
            except:
                messages.success(request, u"Обратите внимание, цены на товары обновлены")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if cart.quantity():
                order = form.save(commit=False)
                statuses = OrderStatus.objects.filter(is_initial=True)
                if statuses:
                    order.status = statuses[0]
                order.total_cost = cart.summary()
                order.save()
                mes = False
                for item in cart:
                    if item.price > 0:
                        OrderItem.objects.create(
                            order=order,
                            product=item.get_item(),
                            price=item.price,
                            quantity=item.quantity,
                        )
                        item.delete()
                    else:
                        mes = True
                if mes:
                    try:
                        messages.success(request, request.message_cart_not_emp)
                    except:
                        messages.success(request, u"В корзине остались товары которые сейчас купить нельзя")

                # cart.clear()
                customer_email(request, order)
                seller_email(request, order)

                messages.success(request, request.message_after_successful_order)

    context = {'form': form, 'cart': cart, 'breadcrumbs': breadcrumbs}

    return render(request, 'order/cart.html', context)



