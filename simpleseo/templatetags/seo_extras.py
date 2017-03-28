# -*- coding: utf-8 -*-
from constance import config
from django import template
from django.contrib.contenttypes.models import ContentType
from flatpages.models import IndexPage
from simpleseo.models import BasicMetadata

register = template.Library()


@register.inclusion_tag('templatetags/seo_head.html', takes_context=False)
def get_seo(element):
    metadata = {'title': config.DEFAULT_TITLE, 'keywords': config.DEFAULT_KEYWORDS, 'description': config.DEFAULT_DESCR, }
    try:
        ### хак для главной страницы, так как рендерится она класом "посмотреть шаблон" и не передается объект главной
        if 'index' == element:
            element = IndexPage.objects.all()[0]
            ### конец хака
        metadata = BasicMetadata.objects.filter(item_model=ContentType.objects.get_for_model(type(element)), item_id=element.pk, )
        if metadata.count() > 0:
            metadata = metadata[0]
            if len(metadata.title) == 0:
                metadata.title = element.get_title()
        else:
            metadata.title = element.get_title()
    except Exception, e:
        print e
    return {'metadata': metadata}