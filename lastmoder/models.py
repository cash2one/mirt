# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


def save_new_time(sender, instance, **kwargs):
    if sender.__name__ not in ('LogEntry','DataExchangeLog','DataExchange','Directory','Product','Feature','Brand','Image','FeatureGroup','FeatureValue','FeaturesOnec','FeatureValueOnec','WebStockProduct',):
        user = User.objects.all()
        if user:
            l = LogEntry(user=user[0], action_flag=2, object_repr=u"Обновлена дата кэша.",change_message=u'Обновлена дата последнего изменения сайта')
            l.save()

pre_save.connect(save_new_time)