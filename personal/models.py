# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from pyadmin import verbose_name_cases


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u"Пользователь", primary_key=True)
    phone = models.CharField(verbose_name=u"моб. телефон", max_length=10, blank=True, null=True, )

    address = models.CharField(verbose_name=u"Индекс", max_length=6, blank=True, null=True)
    city = models.CharField(verbose_name=u"Город", max_length=255, blank=True, null=True)
    street = models.CharField(verbose_name=u'Улица', max_length=255, blank=True, null=True)
    house = models.CharField(verbose_name=u'Дом', max_length=255, blank=True, null=True)
    apartment = models.CharField(verbose_name=u'Квартира', max_length=255, blank=True, null=True)



    def __unicode__(self):
        return u"Профиль пользователя %s" % self.user.username

    class Meta:
        verbose_name = u'профиль пользователя'
        verbose_name_plural = u'Пользователи'


def link_profile(sender, instance, **kwargs):
    try:
        UserProfile.objects.get_or_create(user=instance)
    except UserProfile.MultipleObjectsReturned:
        for u in UserProfile.objects.filter(user=instance): u.delete()
        UserProfile.objects.create(user=instance)


post_save.connect(link_profile, User)
