# -*- coding: utf-8 -*-

from django.db import models
from pyadmin import verbose_name_cases

PLACEHOLDERS = (
    ('phone', u'Телефон'),
    ('email', u'E-mail'),
    ('address', u'адрес'),


)

class Placeholder(models.Model):
    name = models.CharField(verbose_name=u'Название', help_text=u'Уникальное название блока', max_length=255, unique=True, choices=PLACEHOLDERS)
    content = models.TextField(verbose_name=u'Содержимое', blank=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        verbose_name = verbose_name_cases(
            u'HTML блок', (u'HTML блоки', u'HTML блока', u'HTML блоков'),
            gender = 1, change = u'HTML блок', delete = u'HTML блок', add = u'HTML блок'
        )
        verbose_name_plural = verbose_name.plural

