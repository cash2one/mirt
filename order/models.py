# -*- coding: utf-8 -*-
from decimal import Decimal

from catalog.models import Product, WebStock
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.db import models
from django.db.models import permalink

from catalog.templatetags.catalog_filters import format_price
from pyadmin import verbose_name_cases


class Cart(models.Model):
    created_at = models.DateTimeField(verbose_name=u'Дата создания')
    is_checked_out = models.BooleanField(verbose_name=u'Заказ сформирован', default=False)

    class Meta:
        verbose_name = verbose_name_cases(
            u'корзина', (u'корзины', u'корзины', u'корзины'),
            gender = 0, change = u'корзину', delete = u'корзину', add = u'корзину'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('-created_at',)


    def __unicode__(self):
        return unicode(self.created_at)


class CartItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'item' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['item']))
            kwargs['object_id'] = kwargs['item'].pk
            del(kwargs['item'])
        return super(CartItemManager, self).get(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=u'Корзина')
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u'Стоимость единицы товара')
    quantity = models.PositiveIntegerField(verbose_name=u'Количество', default=1)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ContentTypeManager()

    class Meta:
        verbose_name = verbose_name_cases(
            u'элемент корзины', (u'Элементы корзины', u'элементы корзины', u'элементов корзины'),
            gender=2, change=u'элемент корзины', delete=u'элемент корзины', add=u'элемент корзины'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('cart',)


    def __unicode__(self):
        return ''

    def total_price(self):
        return self.quantity * float(self.price)
    total_price = property(total_price)

    def get_item(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_item(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_item, set_item)


class OrderStatus(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    is_initial = models.BooleanField(verbose_name=u'Начальный', default=False)
    is_closing = models.BooleanField(verbose_name=u'Конечный', default=False)
    index_number = models.IntegerField(verbose_name=u'Порядок статуса',default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_cases(
            u'статус заказа', (u'статус заказа', u'статус заказа', u'статус заказа'),
            gender=2, change=u'Статусы заказов', delete=u'Статусы заказов', add=u'Статусы заказов'
        )
        verbose_name_plural = verbose_name.plural


PAYMENT_TYPE = (
    ('cash_payment', u'Наличными, оплата картой в магазине.'),
    ('non_cash_payment', u'Безналичный расчет'),
)

DELIVERY_TYPE = (
    ('self_delivery', u'Самовывоз'),
    ('delivery', u'Доставка'),
)

class Order(models.Model):
    created_at = models.DateTimeField(verbose_name=u'Дата оформления', auto_now_add=True)

    # Данные пок#упател
    full_name = models.CharField(verbose_name=u'Ф.И.О.', max_length=255, blank=True, null=True,)
    # first_name = models.CharField(verbose_name=u'Имя', max_length=255)
    # last_name = models.CharField(verbose_name=u'Фамилия', max_length=255, blank=True, null=True)

    # addition_phone = models.CharField(verbose_name=u'Доп. телефон', max_length=255, blank=True, null=True)


    # Комментарии к заказу


    # Доставка заказа
    delivery_type = models.CharField(verbose_name=u'Способ доставки', max_length=255, choices=DELIVERY_TYPE, blank=True, null=True)
    # region  = models.CharField(verbose_name=u"Регион", max_length=255, blank=True, null=True)

    city = models.CharField(verbose_name=u"Город", max_length=255, blank=True, null=True)
    postal_code = models.CharField(verbose_name=u"Индекс", max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name=u"Адрес", max_length=500, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=255, )
    email = models.EmailField(verbose_name=u'E-mail', blank=True, null=True)
    comment = models.TextField(verbose_name=u'Комментарий к заказу', blank=True)

    street = models.CharField(verbose_name=u'Улица', max_length=255, blank=True, null=True)
    house = models.CharField(verbose_name=u'Дом', max_length=255, blank=True, null=True)
    # building = models.CharField(verbose_name=u'Корпус', max_length=255, blank=True, null=True)
    apartment = models.CharField(verbose_name=u'Квартира', max_length=255, blank=True, null=True)

    # Оплата заказа
    payment_type = models.CharField(verbose_name=u'Способ оплаты', max_length=255, choices=PAYMENT_TYPE, default='cash_payment')

    status = models.ForeignKey(OrderStatus, verbose_name=u'Статус', blank=True, null=True)

    webstock = models.ForeignKey(WebStock, verbose_name=u'Склад',blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_cases(
            u'заказ', (u'Заказ', u'Заказ', u'Заказ'),
            gender=2, change=u'Заказ', delete=u'Заказ', add=u'Заказ'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('-created_at',)

    def get_items(self):
        return list(OrderItem.objects.filter(order=self))

    def __unicode__(self):
        return u'Заказ №%s от %s' % (self.id, self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    product = models.ForeignKey(Product, verbose_name=u'Товар', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(verbose_name=u'Стоимость единицы товара', max_digits=18, decimal_places=2, help_text=u'Стоимость на момент заказа')
    quantity = models.DecimalField(verbose_name=u'Количество', max_digits=18, decimal_places=6)

    #save product name in case it would be delete by carefree admin
    product_name = models.CharField(verbose_name=u'Наименование товара', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_cases(
            u'элемент заказа', (u'Элементы заказов', u'Элементы заказов', u'Элементы заказов'),
            gender=2, change=u'элемент заказов', delete=u'элемент заказов', add=u'элемент заказов'
        )
        verbose_name_plural = verbose_name.plural

    def p_sum(self):
        return format_price(Decimal(float(self.price)*float(self.quantity)))

    def p_quantity(self):
        return format_price(self.quantity)

    def get_absolute_url(self):
        return self.product.get_absolute_url()
    # @permalink
    # def get_absolute_url(self):
    #     if self.product.directory.old_slug:
    #         url = "%s/" % self.product.directory.old_slug
    #     else:
    #         url = "%s/" % self.product.directory.slug
    #         page = self.product.directory
    #         while page.directory:
    #             url = "%(sl)s/%(prev)s" % {"prev": url, "sl": page.directory.slug}
    #             page = page.directory

        return 'product-detail', (), {'slug': url, 'item':self.product.slug}
#        return 'product-detail', (), {'pk': self.product.pk}

    def save(self, *args, **kwargs):
        if not self.product_name and self.product:
            self.product_name = self.product.name
        super(OrderItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Позиция заказа №%s. Наименование: %s, Количество: %s, Стоимость единицы: %s' % (self.order.id, self.product_name, self.quantity, self.price)