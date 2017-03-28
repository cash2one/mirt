# -*- coding: utf-8 -*-

from django.db import models
from pyadmin import verbose_name_cases
from django.db.models.signals import post_delete
from pytils.translit import slugify
from django.utils import timezone

class Blog_Tag(models.Model):
    title = models.TextField(verbose_name=u'Название')
    order = models.SmallIntegerField(verbose_name=u'Порядок отображения', default=0)

    def __unicode__(self):
        return unicode(self.title)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

    class Meta:
        verbose_name = verbose_name_cases(
            u'тег', (u'теги', u'теги', u'тегов'),
            gender = 0, change = u'тег', delete = u'тег', add = u'тег'
        )
        verbose_name_plural = verbose_name.plural


class News(models.Model):
    created_at = models.DateField(verbose_name=u'Дата создания',default=timezone.now)
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    slug = models.SlugField(verbose_name=u"Slug",
                            max_length=100, blank=True,
                            help_text=u'url, может содержать буквы, цифры, знак подчеркивания и дефис')


    short_description = models.TextField(help_text=u'Краткое описание новости', max_length=255, verbose_name=u'Краткое описание', blank=True)
    description = models.TextField(help_text=u'Полный текст новости', verbose_name=u'Текст')

    is_visible = models.BooleanField(verbose_name=u'Отображать', default=True)
    is_visible_main = models.BooleanField(verbose_name=u'Отображать на главной', default=False)
    # is_important = models.BooleanField(verbose_name=u'Важная новость', default=False)

    tags = models.ManyToManyField(Blog_Tag, blank=True, null=True, verbose_name=u"Тэги")

    @models.permalink
    def get_absolute_url(self):
        return 'news:news-detail', (), {'slug': self.slug}

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)
            item = News.objects.filter(slug=self.slug)
            if item:
                self.slug += "_"+str(self.pk)

        super(News, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_cases(
            u'новость', (u'новости', u'новости', u'новостей'),
            gender = 0, change = u'новость', delete = u'новость', add = u'новость'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('-created_at',)

def delete_metadata(sender, instance, **kwargs):
    try:
        from simpleseo.models import BasicMetadata
        BasicMetadata.objects.get(page=instance).delete()
    except:
        pass

post_delete.connect(delete_metadata, News)




