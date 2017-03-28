# -*- coding: utf8 -*-
from constance import config
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from datetime import datetime
from django.template import Template, Context
from django.template.loader import render_to_string
from main import settings
from message.models import Mail
from pyadmin import verbose_name_cases

DATA_EXCHANGE_TYPE = (
    ('importing_catalog', u'загрузка каталога'),
    ('importing_prices', u'загрузка цен товаров'),
    # ('importing_discount_carts', u'загрузка скидок по дисконтным картам'),
)


class ExchangeFTPs(models.Model):
    ftp_ip = models.CharField(verbose_name=u'Адресс FTP', max_length=255)
    login = models.CharField(verbose_name=u'Логин FTP', max_length=255)
    passw = models.CharField(verbose_name=u'Пароль FTP', max_length=255)
    name = models.CharField(verbose_name=u'Условное имя FTP сервера', max_length=255, blank=True, null=True,
                            help_text=u'Будет отображаться в спиcке доступных FTP если заполнено')

    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        return u'%s@%s' % (self.login, self.ftp_ip)

    class Meta:
        verbose_name = verbose_name_cases(
            u'ftp', (u'ftp', u'ftp', u'ftp'),
            gender = 0, change = u'ftp', delete = u'ftp', add = u'ftp'
        )
        verbose_name_plural = u'Настройки FTP'


class DataExchange(models.Model):
    ftp = models.ForeignKey(ExchangeFTPs, verbose_name=u'FTP сервер',
                            help_text=u'С данным FTP будет проходить обмен данными. Если не указан - будет поиск на локальном сервере',
                            blank=True, null=True)
    busy = models.BooleanField(u'Задача в процессе', default=False)
    time_start = models.DateTimeField(verbose_name=u'Дата начала процесса', blank=True, null=True, )
    time_finish = models.DateTimeField(verbose_name=u'Дата окончания процесса', blank=True, null=True, )
    type = models.CharField(verbose_name=u'Тип', max_length=255, choices=DATA_EXCHANGE_TYPE)
    task_id = models.CharField(verbose_name=u'Код задачи', max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, verbose_name=u'Путь',
                            help_text=u'Путь до файла на FTP-сервере или на локальном-сервере(начиная с папки media/upload/data_exchange/). Например: import.xml, ')

    def __unicode__(self):
        return u'%s' % self.get_type_display()

    class Meta:
        verbose_name = verbose_name_cases(
            u'операцию', (u'операции', u'операций', u'операций'),
            gender = 0, change = u'операцию', delete = u'операцию', add = u'операцию'
        )
        verbose_name_plural = u'Операции обмена'
        ordering = ('type',)


class DataExchangeLog(models.Model):
    data = models.ForeignKey(DataExchange, verbose_name=u'Тип обмена')
    time_start = models.DateTimeField(verbose_name=u'Дата и время', blank=True, null=True, auto_now_add=True, )
    message = models.TextField(verbose_name=u'Уведомление', blank=True, null=True, )

    def __unicode__(self):
        for name in DATA_EXCHANGE_TYPE:
            if name[0] == self.data.type:
                return u'%s' % name[1]

    class Meta:
        verbose_name = verbose_name_cases(
            u'запись', (u'записи', u'записи', u'записи'),
            gender = 0, change = u'запись', delete = u'запись', add = u'запись'
        )
        verbose_name_plural = u'Лог обмена'



# Отправка отчёта по результатам обмена данными
def send_information(data_exchange_object, status):
    """
    send email with report of importing catalog
    """
    context = {'log_lines': DataExchangeLog.objects.filter(data=data_exchange_object).order_by('id'), 'data': data_exchange_object,
               'status': status}
    try:
        email_from = settings.DEFAULT_FROM_EMAIL
        mail_to = config.EMAIL_EXCHANGE.replace(' ','').split(',')
        mail_subject = Mail.objects.filter(type="exch_email")[0].subject
        mail_template = Mail.objects.filter(type="exch_email")[0].mail
        mail_message = Template(mail_template).render(Context(context))
        mail = EmailMessage(mail_subject, mail_message, email_from, mail_to)
        mail.content_subtype = 'html'
        mail.send()

    except:
        print 'error send mail'
    return


# Запись информации об обмене данными
def log_event(type_ex, message, status=None):

    data = DataExchange.objects.get(type=type_ex)
    log = DataExchangeLog(data=data, message=message)
    log.save()

    if status:
        if status == 'init':
            if data.busy:
                return True  # Сообщаем что задача в процессе
            else:

                #Очищаем лог
                for log_line in DataExchangeLog.objects.filter(data__type=type_ex):
                    log_line.delete()

                data.busy = True  # Указываем что процесс запущен
            data.time_start = datetime.now()
            data.save()

        if status in ['critical_error', 'success']:
            user = User.objects.all()
            if user:
                l = LogEntry(user=user[0], action_flag=2, object_repr=u"Обновлена дата кэша.",change_message=u'Обновлена дата последнего изменения сайта')
                l.save()
            data.busy = False  # Указываем что процесс не запущен
            data.time_finish = datetime.now()
            data.save()
            send_information(data, status)

    return False#Всё ок


class RunSchedule(models.Model):
    data = models.ForeignKey(DataExchange, verbose_name=u'Тип обмена')
    active = models.BooleanField(verbose_name=u'Активно',default=True,)
    hours = models.IntegerField(verbose_name=u'Час', help_text=u'Пустое поле означает каждый час', blank=True, null=True)
    min = models.IntegerField(verbose_name=u'Минута', help_text=u'Пустое поле означает каждую минуту', blank=True, null=True)

    def __unicode__(self):
        for name in DATA_EXCHANGE_TYPE:
            if name[0] == self.data.type:
                return u'%s' % name[1]

    class Meta:
        verbose_name = verbose_name_cases(
            u'время', (u'время', u'время', u'время'),
            gender = 0, change = u'время', delete = u'время', add = u'время'
        )
        verbose_name_plural = u'Расписание'