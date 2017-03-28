# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from django.db.models.signals import post_delete, post_save
from pyadmin import verbose_name_cases



class FlatPage(MPTTModel):
    TYPES = (
        ('text', u'Текстовая'),
        ('contacts', u'Контакты'),
        ('news', u'Новости'),
        ('announce', u'Анонсы'),
        # ('services', u'Услуги'),
    )

    parent = TreeForeignKey(
        'self',
        related_name='child',
        verbose_name=u'Родительская страница',
        blank=True,
        null=True
    )
    title = models.CharField(
        u'Заголовок',
        max_length=200)

    url = models.CharField(
        verbose_name=u'URL',
        help_text=u'Если указать урл на новость или анонс то данный элемент в меню будет ссылкой',
        max_length=100,
        db_index=True,
        unique=True
    )

    content = models.TextField(
        u'Cодержимое страницы',
        blank=True
    )

    menu_title = models.CharField(
        max_length=255,
        verbose_name=u'Заголовок в меню',
        blank=True,
        null=True,
        help_text=u'Пустое поле будет означать дублирование заголовка страницы'
    )

    type = models.CharField(
        verbose_name=u'Тип',
        help_text=u'Характеризует функционал страницы',
        max_length=255,
        choices=TYPES,
        default='text',
    )

    show_in_menu = models.BooleanField(
        default=False,
        verbose_name=u'Отображать в верхнем меню',
    )

    show_in_side_menu = models.BooleanField(
        default=False,
        verbose_name=u'Отображать в боковом меню'
    )

    show_in_bottom_menu = models.BooleanField(
        default=False,
        verbose_name=u'Отображать в нижнем меню'
    )

    show_in_sub_bottom_menu = models.BooleanField(
        default=False,
        verbose_name=u'Отображать в дополнительном нижнем меню'
    )

    is_visible = models.BooleanField(
        default=True,
        verbose_name=u'Отображать?'
    )

    order = models.IntegerField(
        verbose_name=u'Порядок',
        default=0,
        blank=True,
        null=True
    )

    tree = TreeManager()

    class Meta:
        verbose_name = verbose_name_cases(
            u'элемент сайта', (u'Дерево сайта', u'элементы сайта', u'элементов сайта'),
            gender=2, change=u'элемент', delete=u'элемент', add=u'элемент'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('url',)


    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title

    def get_title(self):
        return self.title

    #TODO: переписать side_menu для flatpages, services и catalog
    #таким образом, чтобы использовать id
    #а потому убрать отсюда этот метод нафиг
    def slug(self):
        return self.url

    @models.permalink
    def get_absolute_url(self):
        url = self.url
        if url.startswith('/'):
            url = url[1:]
        return 'fpc:flatpage-det', (), {'url': url}


    def get_breadcrumbs(self):
        breadcrumbs = []
        for ancestor in self.get_ancestors(include_self=True):
            if ancestor.menu_title:
                ancestor.name = ancestor.menu_title
            else:
                ancestor.name = ancestor.title
            breadcrumbs.append(ancestor)
        return breadcrumbs

    def save(self, *args, **kwargs):
        if not self.url.startswith('/'):
            self.url = '/' + self.url
        if not self.url.endswith('/'):
            self.url += '/'
        if self.type == 'news':
            self.url = '/novosti/'
        if self.type == 'contacts':
            self.url = '/kontakty/'
        if self.type == 'announce':
            self.url = '/anonsy/'
        # if self.type == 'services':
        #     self.url = '/uslugi/'
        super(FlatPage, self).save(*args, **kwargs)

    def get_menu_title(self):
        if self.menu_title:
            return self.menu_title
        return self.title


    def get_absolute_parent(self):
        x = self.parent
        while x.parent:
            x = x.parent
        return x

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = 'order'


def save_fp(sender, instance, **kwargs):
    FlatPage.tree.rebuild()
post_save.connect(save_fp, FlatPage)

class IndexPage(models.Model):
    content = models.TextField(u'Cодержимое', blank=True, null=True)

    def __unicode__(self):
        return u"%s" % u"Главная страница"

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = verbose_name_cases(
            u'главная страница', (u'главная страница', u'главные страницы', u'главных страниц'),
            gender=0, change=u'главную страницу', delete=u'главную страницу', add=u'главную страницу'
        )
        verbose_name_plural = verbose_name.plural


#Тут стандартно. удаляем
def delete_metadata(sender, instance, **kwargs):
    try:
        from simpleseo.models import BasicMetadata
        BasicMetadata.objects.get(page=instance).delete()
    except:
        pass

post_delete.connect(delete_metadata, FlatPage)
post_delete.connect(delete_metadata, IndexPage)


class Advantage(models.Model):
    title = models.CharField(u'Заголовок', max_length=200)
    url = models.CharField(verbose_name=u'URL',
                           help_text=u'Если указать урл на новость или анонс то данный элемент в меню будет ссылкой',
                           max_length=100, db_index=True, unique=True)

    short_description = models.TextField(
        help_text=u'Краткое описание',
        max_length=255,
        verbose_name=u'Краткое описание',
        blank=True
    )

    content = models.TextField(u'Cодержимое страницы', blank=True)

    image = models.ImageField(verbose_name=u'Изображение на главной', blank=True, upload_to='uploads/advantages/', help_text=u'Изображение .jpeg,jpg c размерами 106x93')

    is_visible = models.BooleanField(default=False, verbose_name=u'Отображать?')
    is_visible_on_main = models.BooleanField(default=True, verbose_name=u'Отображать на главной?')
    order = models.IntegerField(verbose_name=u'Порядок',
                                default=0, blank=True, null=True)


    class Meta:
        verbose_name = verbose_name_cases(
            u'преимущество', (u'преимущества', u'преимущества', u'преимуществ'),
            gender=2, change=u'преимущество', delete=u'преимущество', add=u'преимущество'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('order',)

    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title

    def get_title(self):
        return self.title

    def slug(self):
        return self.url

    @models.permalink
    def get_absolute_url(self):
        url = self.url
        if url.startswith('/'):
            url = url[1:]
        return 'fpc:advantage-detail', (), {'url': url}

    def get_breadcrumbs(self):
        return [{"title": self.title}, ]

    def save(self, *args, **kwargs):
        if not self.url.startswith('/'):
            self.url = '/' + self.url
        if not self.url.endswith('/'):
            self.url += '/'
        super(Advantage, self).save(*args, **kwargs)

