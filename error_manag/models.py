# -*- coding: utf-8 -*-
from constance import config

from django.db import models
from django.template import Template, Context
from django.conf import settings
import os
from pyadmin import verbose_name_cases

class ErrorMessage(models.Model):
    CHOICES = (
        ('404', u'404: страница не найдена'),
        ('500', u'500: внутренняя ошибка сервера'),
        ('502', u'502: сервер не отвечает (происходит обноление сайта, база данных перегружена)'),
        ('504', u'504: слишком большое время ожидания запроса'),
        )

    type = models.CharField(choices=CHOICES, max_length=255, verbose_name=u'Тип', unique=True)
    message = models.TextField(verbose_name=u'Текст сообщения', blank = True)

    def __unicode__(self):
        return self.get_type_display()

    def save(self, *args, **kwargs):
        #save the text to the base template
        error_type = self.type
        error_text = self.message
        file0 = open(os.path.join(settings.PROJECT_ROOT, 'templates','error_base.html'), 'r')
        template = Template(file0.read())
        template_name = str(self.type)+'.html'

        file1 = open(os.path.join(settings.PROJECT_ROOT, 'templates', template_name), 'w')
        file1.write("%s" % template.render(Context(locals())).encode('utf8','ignore'))
        file1.close()
        file0.close()

        super(ErrorMessage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_cases(
            u'текст серверных ошибок', (u'текст серверных ошибок', u'текста серверных ошибок', u'текстов серверных ошибок'),
            gender = 1, change = u'текст серверных ошибок', delete = u'текст серверных ошибок', add = u'текст серверных ошибок'
        )
        verbose_name_plural = verbose_name.plural

