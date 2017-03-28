# -*- coding: utf-8 -*- 

from django.db import models
from pyadmin import verbose_name_cases


class Feedback(models.Model):
    created_at = models.DateTimeField(verbose_name=u'Дата создания', auto_now_add=True)
    name = models.CharField(max_length=255, verbose_name=u'Имя', blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name=u'Контактный телефон', blank=True, null=True)
    email = models.EmailField(verbose_name=u'Электронная почта', blank=True, null=True)
    message = models.TextField(verbose_name=u'Сообщение')
    is_closed = models.BooleanField(verbose_name=u'Обработано', default=False)

    def __unicode__(self):
        return u'Сообщение №%s от %s' % (self.id, self.created_at)

    class Meta:
        verbose_name = verbose_name_cases(
            u'cooбщение с формы обратной связи', (u'cooбщение с формы обратной связи', u'cooбщения с формы обратной связи', u'cooбщений с формы обратной связи'),
            gender = 1, change = u'cooбщение с формы обратной связи', delete = u'cooбщение с формы обратной связи', add = u'cooбщение с формы обратной связи'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('-created_at',)

