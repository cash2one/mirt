# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.utils.encoding import python_2_unicode_compatible
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from pyadmin import verbose_name_cases


@python_2_unicode_compatible
class Service(MPTTModel):
    parent = TreeForeignKey('self', related_name='child', verbose_name=u'Родительский сервис', blank=True, null=True)
    title = models.CharField(u'Заголовок', max_length=200)
    url = models.CharField(verbose_name=u'slug',
                           help_text=u'данный урл подставляется к /service/',
                           max_length=100, db_index=True, unique=True)

    content = models.TextField(u'Cодержимое страницы', blank=True)
    menu_title = models.CharField(max_length=255, verbose_name=u'Заголовок в меню',
                                  blank=True, null=True,
                                  help_text=u'Пустое поле будет означать дублирование заголовка страницы')


    is_visible = models.BooleanField(default=True, verbose_name=u'Отображать?')
    # show_in_main = models.BooleanField(default=False, verbose_name=u'Отображать на главной',)
    tree = TreeManager()

    class Meta:
        verbose_name = verbose_name_cases(
            u'услугу', (u'Услуги', u'услуги', u'услуг'),
            gender=2, change=u'услугу', delete=u'услугу', add=u'услугу'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('url',)


    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title

    def get_title(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        url = self.url
        if url.startswith('/'):
            url = url[1:]
        return 'services:service-detail', (), {'slug': url}


    def get_breadcrumbs(self):
        breadcrumbs = []
        for ancestor in self.get_ancestors(include_self=True):
            if ancestor.menu_title:
                ancestor.name = ancestor.menu_title
            else:
                ancestor.name = ancestor.title
            ancestor.url = ancestor.get_absolute_url()
            breadcrumbs.append(ancestor)
        return breadcrumbs


    def get_menu_title(self):
        if self.menu_title:
            return self.menu_title
        return self.title


    def get_absolute_parent(self):
        x = self.parent
        while x.parent:
            x = x.parent
        return x


#Тут стандартно. удаляем
def delete_metadata(sender, instance, **kwargs):
    try:
        from simpleseo.models import BasicMetadata
        BasicMetadata.objects.get(page=instance).delete()
    except:
        pass

post_delete.connect(delete_metadata, Service)