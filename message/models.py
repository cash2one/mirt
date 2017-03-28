# -*- coding: utf8 -*-

from django.db import models
from tinymce import models as tinymce_models
from pyadmin import verbose_name_cases

class Message(models.Model):
    CHOICES = (
        ('message_after_feedback_form', u'после успешной отправки формы обратной связи'),
        ('message_after_adding_the_goods_into_the_basket', u'после добавления товара в корзину'),
        ('message_after_successful_order', u'после успешного оформления заказа'),
        ('message_after_activation_email', u'об отправке письма для активации'),
        ('message_after_successful_authentication', u'об успешной авторизации'),
        ('message_after_password_reset_email', u'об отправке письма для восстановления пароля'),
        ('message_after_successful_profile_saving', u'об успешном сохранении профиля пользователя'),
        ('message_after_successful_password_changing', u'об успешном изменении пароля'),
        ('message_novalid_authentication', u'сообщение о неверном логине или пароле'),
        ('message_after_error_reg', u'сообщение об ошибке регистрации'),
        ('message_logout', u'сообщение о выходе из системы'),
        ('messages_good_edit', u'сообщение об успешном редактирование профиля'),
        ('messages_pass_not_confirm', u'сообщение о том что пароли не совпадают'),
        ('messages_not_valid_password', u'сообщение о том что введён неверно пароль'),
        ('messages_email_not_found', u'сообщение о том что указанный ящик электронной почты не найден в базе'),

    )

    type = models.CharField(choices=CHOICES, max_length=255, verbose_name=u'Тип', unique=True)
    message = models.TextField(verbose_name=u'Текст сообщения', blank = True)

    def __unicode__(self):
        return self.get_type_display()

    def get_absolute_url(self):
        return u"/kontakty/?thanks_for_feedback=true"

    class Meta:
        verbose_name = verbose_name_cases(
            u'уведомление на сайте', (u'уведомление на сайте', u'уведомления на сайте', u'уведомлений на сайте'),
            gender = 0, change = u'уведомление на сайте', delete = u'уведомление на сайте', add = u'уведомление на сайте'
        )
        verbose_name_plural = verbose_name.plural


class Mail(models.Model):
    CHOICES = (
        ('contacts_email', u'письмо с формы обратной связи'),
        ('seller_email', u'письмо менеджеру после оформления заказа'),
        ('customer_email', u'письмо покупателю после оформления заказа'),
        ('exch_email',u'письмо с отчётом обмена'),
        ('activation_email', u'для активации'),
        ('account_activated_email', u'об успешной активации'),
        ('password_reset_email', u'для восстановления пароля'),

        )

    type = models.CharField(choices=CHOICES, max_length=255, verbose_name=u'Тип', unique=True)
    subject = models.CharField(max_length=255, verbose_name=u'Тема письма', blank=True, null=True)
    mail = tinymce_models.HTMLField(verbose_name=u'Текст письма', blank=True)

    def __unicode__(self):
        return self.get_type_display()

    class Meta:
        verbose_name = verbose_name_cases(
            u'уведомление на почту', (u'уведомление на почту', u'уведомления на почту', u'уведомлений на почту'),
            gender = 0, change = u'уведомление на почту', delete = u'уведомление на почту', add = u'уведомление на почту'
        )
        verbose_name_plural = verbose_name.plural
        ordering = ('type',)
