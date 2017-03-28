# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models
from flatpages.models import FlatPage
from announce.models import Announce
from pyadmin import verbose_name_cases


class SeoManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'page' in kwargs:
            kwargs['item_model'] = ContentType.objects.get_for_model(type(kwargs['page']))
            kwargs['item_id'] = kwargs['page'].pk
            del (kwargs['page'])
        return super(SeoManager, self).get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if 'page' in kwargs:
            kwargs['item_model'] = ContentType.objects.get_for_model(type(kwargs['page']))
            kwargs['item_id'] = kwargs['page'].pk
            del (kwargs['page'])
        return super(SeoManager, self).filter(*args, **kwargs)




class BasicMetadata(models.Model):
    CLASSES_WITH_TITLE = (FlatPage, Announce)
    title = models.TextField(blank=True, null=True, verbose_name=u'title')
    keywords = models.TextField(blank=True, null=True, verbose_name=u'keywords')
    description = models.TextField(blank=True, null=True, verbose_name=u'description')
    item_id = models.PositiveIntegerField(verbose_name=u'Идентификатор объекта')
    item_model = models.ForeignKey(ContentType, verbose_name=u'Идентификатор модели')
    objects = SeoManager()

    def __unicode__(self):
        return u''

    def save(self, *args, **kwargs):
        item = self.item_model.model_class().objects.get(id=self.item_id)

        try:
            if len(self.title) == 0:
                if self.item_model.model_class() in self.CLASSES_WITH_TITLE:
                    title = item.title
                else:
                    title = item.__unicode__()
                self.title = title
        except:
            pass
        super(BasicMetadata, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_cases(
            u'сео', (u'сео', u'сео', u'сео'),
            gender = 0, change = u'сео', delete = u'сео', add = u'сео'
        )
        verbose_name_plural = verbose_name.plural
