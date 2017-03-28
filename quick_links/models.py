# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from pytils.translit import slugify
from catalog.models import Product, Directory, Brand
from pyadmin import verbose_name_cases


class ProductGroup(models.Model):
    name = models.CharField(verbose_name=u'Название', help_text=u'Уникальное название быстрой группы',
                        max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        verbose_name = verbose_name_cases(
            u'группа товаров', (u'группы товаров', u'группы товаров', u'группы товаров'),
            gender = 0, change = u'группу товаров', delete = u'группу товаров', add = u'группу товаров'
        )
        verbose_name_plural = verbose_name.plural


    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)


class ProductFromGroup(models.Model):
    group = models.ForeignKey(ProductGroup, verbose_name=u'Название Группы', related_name='Product_from_group')
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)


    def __unicode__(self):
        return u'%s-%s' % (self.group.name, self.product.name)


    class Meta:
        verbose_name = verbose_name_cases(
            u'товар', (u'товары', u'товары', u'товары'),
            gender = 0, change = u'товар', delete = u'товар', add = u'товар'
        )
        verbose_name_plural = verbose_name.plural



class QuickLink(MPTTModel):
    name = models.CharField(verbose_name=u'Название', help_text=u'Уникальное название быстрой ссылки',
                            max_length=255, unique=True)
    parent = models.ForeignKey('self', verbose_name=u'Родительская страница', blank=True,null=True)
    slug = models.SlugField(verbose_name=u"Slug", max_length=100, help_text=u'Наименование ссылки в url',unique=True)
    ol_slug = models.CharField(verbose_name=u"Старый урл", max_length=255, help_text=u'урл вводим без домена. например, если нужно указать - http://dmarket.simplemedia.ru/example/url, в поле пишем только /example/url',blank=True,null=True)

    description_up = models.TextField(verbose_name=u'Описание над товарами', blank=True, null=True, help_text=u'Текст описания ссылки')
    description_down = models.TextField(verbose_name=u'Описание под товарами', blank=True, null=True, help_text=u'Текст описания ссылки')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    is_visible = models.BooleanField(verbose_name=u'Отображать', default=True)
    # is_important = models.BooleanField(verbose_name=u'Основная', default=True, help_text=u'При отображении не будет свёрнута')

    tree = TreeManager()

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = 'order'

    def __unicode__(self):
        return u'%s' % (self.name,)

    def get_children(self):
        return QuickLink.objects.filter(parent=self, is_visible=True)

    def get_breadcrumbs(self):
        list = []
        item = self.parent
        while item:
            list.append({"title": item.name, "url": item.get_absolute_url})
            item = item.parent
        list.append({"title": self.name})
        return list

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super(QuickLink, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'quick_link', (), {'slug': self.slug}

    class Meta:
        verbose_name = verbose_name_cases(
            u'посадочная страница', (u'посадочная страница', u'посадочная страница', u'посадочная страница'),
            gender = 0, change = u'посадочную страница', delete = u'посадочную страница', add = u'посадочную страница'
        )
        verbose_name_plural = verbose_name.plural


class QuickProductLink(models.Model):
    quick_link = models.ForeignKey(QuickLink, verbose_name=u'Название ссылки', related_name='product_link')
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    def __unicode__(self):
        return u'%s-%s' % (self.quick_link.name, self.product.name)



    class Meta:
        verbose_name = verbose_name_cases(
            u'товар', (u'товары', u'товары', u'товары'),
            gender = 0, change = u'товар', delete = u'товар', add = u'товар'
        )
        verbose_name_plural = verbose_name.plural


class QuickDirectoryLink(models.Model):
    quick_link = models.ForeignKey(QuickLink, verbose_name=u'Название ссылки', related_name='directory_link')
    directory = models.ForeignKey(Directory, verbose_name=u'Раздел')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    def __unicode__(self):
        return u'%s-%s' % (self.quick_link.name, self.directory.name)


    class Meta:
        verbose_name = verbose_name_cases(
            u'раздел', (u'разделы каталога', u'разделы каталога', u'разделов каталога'),
            gender = 0, change = u'раздел', delete = u'раздел', add = u'раздел'
        )
        verbose_name_plural = verbose_name.plural


class QuickBrandLink(models.Model):
    quick_link = models.ForeignKey(QuickLink, verbose_name=u'Название ссылки', related_name='brand_link')
    brand = models.ForeignKey(Brand, verbose_name=u'Брэнд')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    def __unicode__(self):
        return u'%s-%s' % (self.quick_link.name, self.brand.name)

    class Meta:
        verbose_name = verbose_name_cases(
            u'бренд', (u'бренды', u'бренды', u'брэнды'),
            gender = 0, change = u'бренд', delete = u'бренд', add = u'бренд'
        )
        verbose_name_plural = verbose_name.plural


class QuickGroupLink(models.Model):
    quick_link = models.ForeignKey(QuickLink, verbose_name=u'Название ссылки', related_name='group_link')
    group = models.ForeignKey(ProductGroup, verbose_name=u'Группа')
    order = models.SmallIntegerField(verbose_name=u'Порядок', default=0)

    def __unicode__(self):
        return u'%s-%s' % (self.quick_link.name, self.group.name)

    class Meta:
        verbose_name = verbose_name_cases(
            u'группа товаров', (u'группы товаров', u'группы товаров', u'группы товаров'),
            gender = 0, change = u'группу товаров', delete = u'группу товаров', add = u'группу товаров'
        )
        verbose_name_plural = verbose_name.plural

def save_fp(sender, instance, **kwargs):
    QuickLink.tree.rebuild()
post_save.connect(save_fp, QuickLink)