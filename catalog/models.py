# -*- coding: utf-8 -*-
import json
import os
from constance import config
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_delete
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.models import MPTTModel
from pytils.translit import slugify
from main import settings

try:
    from catalog.templatetags.catalog_filters import format_price
    from pyadmin import verbose_name_cases
except:
    pass

class Accessories(models.Model):
    name    = models.CharField(max_length=255, verbose_name=u'Наименование раздела аксессуаров')

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_cases(
            u'раздел', (u'разделы аксессуаров', u'разделы аксессуаров', u'разделов аксессуаров'),
            gender = 0, change = u'раздел', delete = u'раздел', add = u'раздел'
        )
        verbose_name_plural = verbose_name.plural


class Directory(MPTTModel):
    name = models.CharField(max_length=255, verbose_name=u'Наименование раздела')
    singular_name = models.CharField(max_length=255, verbose_name=u'Наименование раздела в единственном числе', blank=True, null=True)
    directory = TreeForeignKey('self', related_name='subdirectory', verbose_name=u'Родительский раздел', blank=True, null=True)
    image = models.ImageField(verbose_name=u'Изображение', upload_to='uploads/catalog/', blank=True, null=True,help_text=u'Картинка будет ужата до размера ')
    is_visible = models.BooleanField(verbose_name=u'Отображать', default=True)
    show_in_bottom_menu = models.BooleanField(verbose_name=u'Отображать в нижнем меню', default=False)
    order = models.SmallIntegerField(verbose_name=u'Порядок отображения', default=0)
    slug = models.SlugField(verbose_name=u"Slug", max_length=100, blank=True, help_text=u'Наименование раздела в url, может содержать буквы, цифры, знак подчеркивания и дефис')

    top_description = models.TextField(verbose_name=u'Описание, отображаемое в верхней части страницы', blank=True, null=True)
    bottom_description = models.TextField(verbose_name=u'Описание, отображаемое в нижней части страницы', blank=True, null=True)

    seo_title = models.TextField(verbose_name=u'Заголовок', blank=True, null=True,
                                 help_text=u'Используйте теги #directory# (название раздела каталога), #brand# (бренд товара), #name# (название товара) для шаблонного задания SEO настроек')
    seo_description = models.TextField(verbose_name=u'Описание', blank=True, null=True,
                                       help_text=u'Используйте теги #directory# (название раздела каталога), #brand# (бренд товара), #name# (название товара) для шаблонного задания SEO настроек')
    seo_keywords = models.TextField(verbose_name=u'Ключевые слова', blank=True, null=True,
                                    help_text=u'Используйте теги #directory# (название раздела каталога), #brand# (бренд товара), #name# (название товара) для шаблонного задания SEO настроек')
    tree = TreeManager()

    accessory = models.ManyToManyField(Accessories, verbose_name=u'Раздел группы аксессуаров', blank=True, null=True)
    dir_accessory = TreeManyToManyField('self', related_name='access_directories', verbose_name=u'Раздел каталога акссесуаров', symmetrical=False, blank=True, null=True)

    onec = models.CharField(verbose_name=u'Код в 1С', max_length=255, blank=True, null=True,)

    @models.permalink
    def get_absolute_url(self):
        url = "%s/" % self.slug
        page = self
        while page.directory:
            url = "%(sl)s/%(prev)s" % {"prev": url, "sl": page.directory.slug}
            page = page.directory
        return 'catalog:directory-detail', (), {'slug': url}

    def __unicode__(self):
        return u'%s'%self.name

    #TODO: унифицировать с таким же методом в flatpages, services
    def get_breadcrumbs(self):
        breadcrumbs = []
        for ancestor in self.get_ancestors(include_self=True):
            breadcrumbs.append({"title":ancestor.name, "url": ancestor.get_absolute_url})
        return breadcrumbs

    def get_menu_title(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
            directory = Directory.objects.filter(directory=self.directory, slug=self.slug)
            if directory:
                self.save()
                self.slug += "_"+str(self.pk)
        super(Directory, self).save(*args, **kwargs)

    def get_title(self):
        return u'%s'%self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

    class Meta:
        verbose_name = verbose_name_cases(
            u'раздел', (u'разделы каталога', u'разделы каталога', u'разделов каталога'),
            gender = 0, change = u'раздел', delete = u'раздел', add = u'раздел'
        )
        verbose_name_plural = verbose_name.plural

    class MPTTMeta:
        parent_attr = 'directory'
        order_insertion_by = 'order'


def save_directory(sender, instance, **kwargs):
    pass
    #print sender
    #Directory.tree.rebuild()
post_save.connect(save_directory, Directory)


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Наименование')
    image = models.ImageField(verbose_name=u'Изображение', upload_to='uploads/catalog/', blank=True, null=True)
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255, blank=True, default=True,)

    @models.permalink
    def get_absolute_url(self):
        return 'brand-detail', (), {'pk': self.pk, 'page': 1}

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_cases(
            u'бренд', (u'бренды', u'бренды', u'брэнды'),
            gender = 0, change = u'бренд', delete = u'бренд', add = u'бренд'
        )
        verbose_name_plural = verbose_name.plural


class Product(models.Model):
    created_at = models.DateTimeField(verbose_name=u'Дата добавления', auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name=u'Наименование',)

    articul = models.CharField(max_length=255, verbose_name=u'Артикул', blank=True, null=True,)
    onec = models.CharField(max_length=255, verbose_name=u'Код 1С товара', blank=True, null=True,)
    onecdir = models.CharField(max_length=255, verbose_name=u'Код 1С раздела', blank=True, null=True,)
    searchfield = models.CharField(max_length=255, verbose_name=u'Название для поиска', blank=True, null=True,)

    directory = models.ForeignKey('Directory', verbose_name=u'Раздел каталога',)
    brand = models.ForeignKey('Brand', verbose_name=u'Бренд', blank=True, null=True,)
    price = models.DecimalField(verbose_name=u'Стоимость', decimal_places=2, max_digits=10, default=0)
    description = models.TextField(help_text=u'Описание наименования товара', verbose_name=u'Описание', blank=True)
    short_description = models.CharField(max_length=255, verbose_name=u'Краткое описание над контентом', blank=True, null=True)
    is_visible = models.BooleanField(verbose_name=u'Отображать', default=True)
    slug = models.SlugField(verbose_name=u"Slug", max_length=255, blank=True, help_text=u'Наименование товара в url, может содержать буквы, цифры, знак подчеркивания и дефис')
    show_on_main = models.BooleanField(verbose_name=u'Отображать на главной', default=False)
    accessory = models.ForeignKey(Accessories, related_name='access_product', verbose_name=u'Раздел аксессуаров', blank=True, null=True)

    def entry(self):
        return u'%s'%self.name

    @models.permalink
    def get_absolute_url(self):
        url = "%s/" % self.directory.slug
        page = self.directory
        while page.directory:
            url = "%(sl)s/%(prev)s" % {"prev": url, "sl": page.directory.slug}
            page = page.directory

        return 'catalog:product-detail', (), {'slug': url, 'item':self.slug}

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
            product = Product.objects.filter(directory=self.directory, slug=self.slug)
            if product:
                self.slug += "_"+str(self.pk)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_cases(
            u'товар', (u'товары', u'товары', u'товары'),
            gender = 0, change = u'товар', delete = u'товар', add = u'товар'
        )
        verbose_name_plural = verbose_name.plural

        ordering = ('price',)

    def get_breadcrumbs(self):
        breadcrumbs = [] + self.directory.get_breadcrumbs()
        breadcrumbs.append({"title": self.name})
        return breadcrumbs

    def get_primary_image(self):
        images = Image.objects.filter(product=self, is_primary=True)
        if images.exists():
            image = images[0]
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, image.file.path.encode('utf8', 'ignore'))):
                return image
        return None

    def get_images(self):
        return Image.objects.filter(product=self, is_primary=False)

    def get_secondary_images(self):
        return Image.objects.filter(product=self, is_primary=False)

    def get_features(self):
        return FeatureValue.objects.filter(product=self)

    def get_price(self):
        if self.price>0:
            return format_price(self.price)
        return

    def get_simillar(self):
        try:
            margin = float(config.CATALOG_PRICE_RANGE)
        except:
            margin = 10.
        price = float(self.price)
        return Product.objects.filter(directory=self.directory,
                                      is_visible=True,
                                      price__gte=price*(100.-margin)/100,
                                      price__lte=price*(100.+margin)/100).exclude(id=self.id)

    #Инфа о складах
    def get_stocks_data(self):
        #склады с кол-вом товаров
        items = []

        #данные для маркеров на карте
        map_data = []

        stock_products = {
            i[0]: i[1] for i in WebStockProduct.objects.filter(
                product=self,
                count__gt=0
            ).values_list(
                "webstock__id",
                "count"
            )
        }

        webstocks = WebStock.objects.filter(id__in=stock_products.keys())

        for item in webstocks:
            item.count = stock_products.get(item.id)
            items.append(item)
            if item.lat and item.long:
                map_data.append({
                    "id": item.id,
                    "coordinates": [item.lat, item.long],
                })

        if len(map_data) > 0:
            map_data = json.dumps(map_data)

        return items, map_data


class ProductAccessory(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Продукт',related_name='for_product',)
    accessory = models.ForeignKey(Product, verbose_name=u'Акксесуар', related_name='added_accessory',)

    class Meta:
        verbose_name = verbose_name_cases(
            u'аксессуар', (u'единичные аксесуары', u'единичные аксесуары', u'единичные аксесуары'),
            gender = 0, change = u'аксессуар', delete = u'аксессуар', add = u'аксессуар'
        )
        verbose_name_plural = verbose_name.plural

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "accessory__name__icontains",)


class ImageManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ImageManager, self).get(*args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ImageManager, self).get_or_create(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ImageManager, self).filter(*args, **kwargs)


class Image(models.Model):
    file = models.ImageField(verbose_name=u'Файл', upload_to='uploads/catalog/', help_text=u'Минимальный размер изображения - 160x121 пикселей', null=True)
    name = models.CharField(max_length=255, verbose_name=u'Название', blank=True, null=True)
    is_primary = models.BooleanField(verbose_name=u'Основное изображение', default=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ImageManager()

    def __unicode__(self):
        return '%s' % self.pk

    def get_item(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_item(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    item = property(get_item, set_item)

    class Meta:
        verbose_name = verbose_name_cases(
            u'изображение', (u'изображения', u'изображения', u'изображения'),
            gender = 0, change = u'изображение', delete = u'изображение', add = u'изображение'
        )
        verbose_name_plural = verbose_name.plural


class Promotion(models.Model):
    PROMOTION_TYPE = (
                     ('sale', u'Лучшая цена'),
                     ('new', u'Новинки'),
                     ('special', u'Специальное предложение'),)

    product = models.ForeignKey('Product', verbose_name=u'Товар')
    type = models.CharField(verbose_name=u'Тип', max_length=255, choices=PROMOTION_TYPE)
    description = models.TextField(help_text=u'Описание акции', verbose_name=u'Описание', blank=True)
    start_at = models.DateField(verbose_name=u'Дата начала', blank=True, null=True)
    finish_at = models.DateField(verbose_name=u'Дата окончания', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.get_type_display()

    def get_breadcrumbs(self):
        return [{"title": self.get_type_display()}]

    class Meta:
        verbose_name = verbose_name_cases(
            u'акция', (u'акции', u'акции', u'акции'),
            gender = 0, change = u'акцию', delete = u'акцию', add = u'акцию'
        )
        verbose_name_plural = verbose_name.plural


class FeatureGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название')
    directory = models.ForeignKey('Directory', related_name='group', verbose_name=u'Раздел каталога')

    def __unicode__(self):
        string = "%s" % self.name
        for ancestor in self.directory.get_ancestors(include_self=True, ascending=True):
            string = "%(now)s, %(prev)s" % {"prev": string, "now": ancestor.name}
        return string

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)



    class Meta:
        verbose_name = verbose_name_cases(
            u'группа', (u'группы характеристик', u'группы характеристик', u'группы характеристик'),
            gender = 0, change = u'группу', delete = u'группу', add = u'группу'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('name',)


WIDGET_TYPE = (
    ('fader_double', u'слайдер'),
    ('select_box', u'выпадающий список'),
    ('checkbox', u'выбор элемента'),
    )


class Feature(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название',)
    group = models.ForeignKey('FeatureGroup', verbose_name=u'Группа и раздел каталога')
    widget_type = models.CharField(verbose_name=u'Тип виджета', max_length=255, choices=WIDGET_TYPE, default='checkbox',)
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0,)
    is_primary = models.BooleanField(verbose_name=u'Основная характеристика', default=False,)
    is_filter = models.BooleanField(verbose_name=u'Участвует в фильтрации', default=False,)
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255, blank=True, default=True,)

    def __unicode__(self):
        return u"%s - %s" % (self.group.name,self.name)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains","group__name__icontains","group__directory__name__icontains",)

    class Meta:
        verbose_name = verbose_name_cases(
            u'характеристика', (u'характеристики', u'характеристики', u'характеристики'),
            gender = 0, change = u'характеристику', delete = u'характеристику', add = u'характеристику'
        )
        verbose_name_plural = verbose_name.plural


class FeatureValueGroup(models.Model):
    feature = models.ForeignKey(Feature, related_name='value_group', verbose_name=u'Характеристика')
    name = models.CharField(max_length=255, verbose_name=u'Название')
    regexp = models.CharField(verbose_name=u'Регулярное выражение', max_length=255)
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    def __unicode__(self):
        return self.regexp

    class Meta:
        verbose_name = verbose_name_cases(
            u'группа значений характеристик', (u'группа значений характеристик', u'группа значений характеристик', u'группа значений характеристик'),
            gender = 0, change = u'группу', delete = u'группу', add = u'группу'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('order',)


class FeatureValue(models.Model):
    product = models.ForeignKey('Product', related_name='product_id_for_value', verbose_name=u'Товар',)
    feature = models.ForeignKey('Feature', related_name='value',  verbose_name=u'Характеристика')
    value = models.CharField(verbose_name=u'Значение', max_length=100, blank=True, null=True,)
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255, blank=True, default=True,)

    def __unicode__(self):
        return '%s' % self.value

    class Meta:
        verbose_name = verbose_name_cases(
            u'значения характеристик', (u'значения характеристик', u'значения характеристик', u'значений характеристик'),
            gender = 0, change = u'значение', delete = u'значение', add = u'значение'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('feature__order', 'feature__name')


# Вспомогательная таблица характеристик
class FeaturesOnec(models.Model):
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255, blank=True, default=True,)
    name = models.CharField(verbose_name=u'Название', max_length=255, blank=True, null=True,)
    type_val = models.CharField(verbose_name=u'Тип значений',max_length=255, blank=True, null=True,)

    def __unicode__(self):
        return '%s' % self.value

    class Meta:
        verbose_name = verbose_name_cases(
            u'значения характеристик', (u'значения характеристик вспомогательная', u'значения характеристик', u'значений характеристик'),
            gender = 0, change = u'значение', delete = u'значение', add = u'значение'
        )
        verbose_name_plural = verbose_name.plural


# Вспомогательная таблица значений характеристик
class FeatureValueOnec(models.Model):
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255, blank=True, default=True,)
    feature = models.ForeignKey(FeaturesOnec, related_name='value_onec',  verbose_name=u'Характеристика')
    value = models.CharField(verbose_name=u'Значение', max_length=100, blank=True, null=True,)
    brand = models.BooleanField(verbose_name=u'Бренд', default=False,)

    def __unicode__(self):
        return '%s' % self.value

    class Meta:
        verbose_name = verbose_name_cases(
            u'значения характеристик', (u'значения характеристик вспомогательная', u'значения характеристик', u'значений характеристик'),
            gender = 0, change = u'значение', delete = u'значение', add = u'значение'
        )
        verbose_name_plural = verbose_name.plural


class WebStock(models.Model):
    name = models.CharField(verbose_name=u'Название склада на сайте', max_length=255,)

    address = models.CharField(verbose_name=u'Адрес', max_length=500, blank=True, null=True)
    lat = models.CharField(verbose_name=u'Широта, google map', max_length=255, blank=True, null=True)
    long = models.CharField(verbose_name=u'Долгота, google map', max_length=255, blank=True, null=True)

    mode = models.CharField(verbose_name=u'Часы работы', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=255, blank=True, null=True)

    text = models.TextField(verbose_name=u'Описание склада', max_length=5000, blank=True,null=True)

    def __unicode__(self):
        return '%s' % self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

    class Meta:
        verbose_name = verbose_name_cases(
            u'склад на сайте', (u'склады на сайте', u'склады на сайте', u'складов на сайте'),
            gender = 0, change = u'склад', delete = u'склад', add = u'склад'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('name',)


class WebStockProduct(models.Model):
    webstock = models.ForeignKey(WebStock, verbose_name=u'Cклад на сайте',)
    product = models.ForeignKey(Product, verbose_name=u'Продукт',)
    count = models.FloatField(verbose_name=u'Количество', default=0.0,)

    def __unicode__(self):
        return '%s' % self.product.name

    class Meta:
        verbose_name = verbose_name_cases(
            u'привязку продукта', (u'На складе', u'привязки продуктов', u'привязки продуктов'),
            gender = 0, change = u'склад', delete = u'склад', add = u'склад'
        )
        verbose_name_plural = verbose_name.plural


class OneCstock(models.Model):
    webstock = models.ForeignKey(WebStock, verbose_name=u'Cклад на сайте',)
    onec = models.CharField(verbose_name=u'Код 1С', max_length=255,)

    def __unicode__(self):
        return '%s' % self.onec

    class Meta:
        verbose_name = verbose_name_cases(
            u'код склада в 1С', (u'склады с 1С', u'склады с 1С', u'склады с 1С'),
            gender = 0, change = u'склад', delete = u'склад', add = u'склад'
        )
        verbose_name_plural = verbose_name.plural


class DeleteProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Продукт',)

    def __unicode__(self):
        return '%s' % self.product.name

    class Meta:
        verbose_name = verbose_name_cases(
            u'товар на удаление', (u'товары на удаление', u'товаров на удаление', u'товаров на удаление'),
            gender = 0, change = u'товар', delete = u'товар', add = u'товар'
        )
        verbose_name_plural = verbose_name.plural