# -*- coding: utf-8 -*-
import os
import shutil
from decimal import Decimal

from django.conf import settings
from ftplib import FTP
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from lxml import etree
from django.db import connection, transaction
from pytils.translit import slugify
from data_exchange.models import DataExchange, log_event, DataExchangeLog
from catalog.models import Directory, Product, FeatureValueOnec, FeatureValue, Feature, Brand, FeaturesOnec, FeatureGroup, \
    Image, WebStockProduct, OneCstock, WebStock
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def check_used_slug(slug='', klass_manager=None):
    count_use = klass_manager.objects.filter(slug=slug).count()
    if count_use != 0:
        return klass_manager.objects.filter(slug=slug).order_by('-id')[0].id
    return


# Класс директории
class XmlGoods(object):
    def __init__(self, name='', gid='', parent=''):
        self.name = name
        self.gid = gid
        self.parent = parent


# класс продукта для цен и остатков
class XmlProduct(object):
    def __init__(self, name='', pid='', price='', articul='', sku='', shid='', cat_id='', countall='', description='',
                 photos=[],
                 ambars=[], props=[]):
        self.name = name
        self.pid = pid
        self.cat_id = cat_id
        self.shid = shid
        self.articul = articul
        self.sku = sku
        self.ambars = ambars
        self.photos = photos
        self.props = props
        self.price = price
        self.description = description
        self.countall = countall


# Обработка элементов и создание объектов дериктории
def parsegroup(elem):
    g = XmlGoods()
    for e in elem.iterchildren():
        if e.tag == u'Ид':
            g.gid = u'%s' % e.text

        if e.tag == u'Наименование':
            g.name = u'%s' % e.text
        if e.tag not in [u'Ид', u'Наименование', u'Группы']:
            return None
    return g


def parse_product_price(p):
    try:
        priceinfo = Product.objects.get(onec=p.pid)
    except Product.DoesNotExist:
        log_event('importing_prices', u'Не найден продукт %s по ИД коду %s' % (p.name, p.pid))
        return

    try:
        priceinfo.quantity = float(p.countall)
        if float(p.countall) == 0.0:
            log_event('importing_prices', u'Удаляем продукт %s, так как его нет в наличие ни на одном из складов' % p.pid)
            priceinfo.delete()
            return
        else:
            priceinfo.is_visible = True

    except:
        log_event('importing_prices', u'Указано количество не в цифровом формате у продукта %s' % p.pid)
        return


    try:
        priceinfo.price = Decimal(p.price)
    except:
        log_event('importing_prices', u'Указана цена не в цифровом формате у продукта %s' % p.pid)
        return

    priceinfo.save()

    for w in WebStockProduct.objects.filter(product=priceinfo):
        w.delete()

    for am in p.ambars:
        try:
            co = float(am['count'])
        except Exception,e:
            print e

        try:
            webstock = OneCstock.objects.get(onec=am['aid']).webstock
        except OneCstock.DoesNotExist:
            log_event('importing_prices', u'Не найден склад %s для продукта %s' % (am['aid'], p.pid))
            continue

        try:
            skl, created = WebStockProduct.objects.get_or_create(product=priceinfo, webstock=webstock)
            if created:
                skl.count = co
            else:
                all_co = 0.
                for all_co_am in WebStockProduct.objects.filter(product=priceinfo,
                                                                webstock=webstock).values_list('count', flat=True):
                    all_co += all_co_am
                skl.count = all_co + co

            skl.save()

        except Exception, e:
            log_event('importing_prices',
                      u'Привязка склада %s для продукта %s не удалась (%s)' % (am['aid'], p.pid, e))

            continue

    return


def xml_to_sklads(path_to_file):
    log_event('importing_prices', u'Парсинг XML файла по тегу "Предложение"')
    try:
        for action, elem in etree.iterparse(path_to_file, tag=u'Предложение'):
            if action == 'end':
                p = XmlProduct()
                ambars = []
                for e in elem.iterchildren():
                    if e.tag == u'Ид':
                        p.pid = u'%s' % e.text

                    if e.tag == u'Наименование':
                        p.name = u'%s' % e.text

                    if e.tag == u'Количество':
                        p.countall = u'%s' % e.text

                    if e.tag == u'Цены':
                        for ep in e.iterchildren():
                            for epp in ep.iterchildren():
                                if epp.tag == u'ЦенаЗаЕдиницу':
                                    p.price = u'%s' % epp.text

                    if e.tag == u'Склад':
                        ambars.append({'aid': e.get(u'ИдСклада'), 'count': e.get(u'КоличествоНаСкладе')})
                p.ambars = ambars
                if p.pid !='' and p.name!='':
                    parse_product_price(p)
                elem.clear()
    except Exception, e:
        log_event('importing_prices', u'Критическая ошибка файла XML')
        log_event('importing_prices', u'%s'%e,'critical_error')

    return


def catalog_to_db(a):
    directory, new = Directory.objects.get_or_create(onec=a.gid, name=a.name)
    if new:
        name_temp = slugify(a.name)
        # чек на повтор
        last_id = check_used_slug(name_temp, Directory)
        if last_id:
            name_temp = '%s_%s' % (slugify(a.name), last_id)
        directory.slug = name_temp
        directory.save()
    return


def xml_to_catalog(path_to_file):
    all_g = []  # Список объектов спарсеных директорий
    log_event('importing_catalog', u'Парсинг XML файла по тегу "Группа"')
    iteration = 0
    try:
        etree_gens = etree.iterparse(path_to_file, tag=u'Группа')
        for action, elem in etree_gens:
                if action == 'end':
                    iteration += 1
                    x = parsegroup(elem)
                    if x:
                        parent = elem.getparent().getparent()
                        if parent is not None:
                            x_parent = parsegroup(parent)
                            if x_parent:
                                x.parent = x_parent
                                all_g.append(x)
                        catalog_to_db(x)
                        elem.clear()

        log_event('importing_catalog', u'Указываем родительские разделы')
        for a in all_g:
                if a.gid and a.parent.gid:
                    try:
                        category = Directory.objects.get(onec=a.gid)
                        category.directory = Directory.objects.get(onec=a.parent.gid)
                        category.save()
                    except Directory.DoesNotExist:
                        log_event('importing_catalog', u'Ошибка привязки раздела %s к родительскому %s' % (a.gid, a.parent.gid),
                                  'error')
        log_event('importing_catalog', u'Перепостроение дерева разделов')
        Directory.tree.rebuild()

    except Exception, e:
        log_event('importing_catalog', u'Критическая ошибка синтаксиса XML')
        log_event('importing_catalog', u'%s'%e,'critical_error')
        return
    return


def variant_to_db(a):
    property = FeaturesOnec.objects.filter(onec=a['id'])
    if property:
        property = property[0]
    else:
        property = FeaturesOnec(onec=a['id'], name=a['name'])
        if 'type_val' in a:
            property.type_val = a['type_val']
        else:
            if len(a['variants'])>0:
                property.type_val = u'Справочник'
        property.save()

    if a['variants']:
        for v in a['variants']:
            propertyval = FeatureValueOnec.objects.filter(feature=property, onec=v['id'])
            if propertyval:
                propertyval = propertyval[0]
            else:
                propertyval = FeatureValueOnec(feature=property, onec=v['id'])
            propertyval.value = v['name']
            propertyval.save()
    return


# Свойства и значения свойств
def xml_props_words(path_to_file):
    log_event('importing_catalog', u'Парсинг XML файла по тегу "Свойство"')
    try:
        etree_gens = etree.iterparse(path_to_file, tag=u'Свойство')
        for action, elem in etree_gens:
            if action == 'end':
                p = {}
                variants = []
                for e in elem.iterchildren():
                    if e.tag == u'Ид':
                        p['id'] = u'%s' % e.text

                    if e.tag == u'Наименование':
                        p['name'] = u'%s' % e.text

                    if e.tag == u'ТипЗначений':
                        p['type_val'] = u'%s' % e.text

                    if e.tag == u'ВариантыЗначений':
                        for ep in e.iterchildren():
                            variant = {}
                            for epp in ep.iterchildren():
                                if epp.tag == u'ИдЗначения':
                                    variant['id'] = u'%s' % epp.text

                                if epp.tag == u'Значение':
                                    variant['name'] = u'%s' % epp.text
                            variants.append(variant)
                p['variants'] = variants
                variant_to_db(p)
                elem.clear()
    except Exception, e:
        log_event('importing_catalog', u'Критическая ошибка синтаксиса XML (возможно фаил перезалит)')
        log_event('importing_catalog', u'%s'% e, 'critical_error')
    return


def parse_photos(pxml, product):
    # фотографии
    if len(pxml.photos) > 0:
        first = True
        for photo in pxml.photos:
            photo = 'uploads/%s'%photo
            # если в базе вдруг есть дубли картинок, то устраняем беду.
            if Image.objects.filter(product=product, file=photo,).count() > 1:
                for pd in Image.objects.filter(product=product, file=photo)[1:]:
                    pd.delete()
            # если в базе не больше 1 картинки то или получаем или создаём её.
            try:
                proimg, createdimg = Image.objects.get_or_create(product=product, file=photo, is_primary=first)
                if first:
                    first = False
                if createdimg:
                    proimg.save()
            except Exception, e:
                log_event('importing_catalog', u'Невозможно сохранить картинку %s'%e)
            pass
    return


def parse_specs(pxml, product):
    # характеристики
    for spec in pxml.props:
        if 'value' in spec and 'id' in spec:
            if len(spec['value']) > 0 and spec['value'] != u'None':
                try:
                    property = FeaturesOnec.objects.get(onec=spec['id'])
                except MultipleObjectsReturned:
                    property = FeaturesOnec.objects.filter(onec=spec['id'])[0]
                    log_event('importing_catalog',
                              u'Дублируеться характеристика %s' % spec['id'],
                              'error')
                except Exception,e:
                    log_event('importing_catalog',
                              u'Невозможно найти характеристику из справочника %s %s' % (spec['id'],e),
                              'error')
                    continue

                feature_name = u'%s'% property.name

                #Обрабатываем как бренд
                if feature_name == u'Производитель':
                    try:
                        property_db = FeatureValueOnec.objects.get(onec=spec['value'])
                    except MultipleObjectsReturned:
                        property_db = FeatureValueOnec.objects.filter(onec=spec['value'])[0]
                    except Exception,e:
                        log_event('importing_catalog', u'Невозможно найти характеристику из справочника %s 2%s' % (spec['id'],e),
                                  'error')
                        continue
                    brand, c = Brand.objects.get_or_create(onec=spec['value'],name=property_db.value)
                    if c:
                        brand.save()
                        log_event('importing_catalog', u'Добавлен новый бренд %s' % property_db.value)

                    product.brand = brand
                    product.save()
                    continue

                #Привязываем по фиксированным значениям
                elif property.type_val == u'Справочник':
                    try:
                        property_db = FeatureValueOnec.objects.get(onec=spec['value'])
                    except MultipleObjectsReturned:
                        property_db = FeatureValueOnec.objects.filter(onec=spec['value'])[0]
                    except Exception,e:
                        log_event('importing_catalog', u'Невозможно найти характеристику из справочника %s 1%s' % (spec['id'],e),
                                  'error')
                        continue
                    feature_value = property_db.value
                    feature_type = 'checkbox'

                #Привязываем как числовой значение
                elif property.type_val == u'Число':
                    feature_value = float(spec['value'])
                    feature_type = 'fader_double'
                else:

                    #Привязываем как булевое значение
                    if spec['value'] =='true':
                        feature_value = u'Есть'
                        feature_type = 'checkbox'
                    elif spec['value'] =='false':
                        feature_value = u'Нет'
                        feature_type = 'checkbox'
                    else:
                        #Привязываем как строковое значение
                        feature_value = spec['value']
                        feature_type = 'select_box'


                if product.directory:
                    # Получаем или создаём характеристику в этом разделе.
                    group, created = FeatureGroup.objects.get_or_create(name=u'Основная', directory=product.directory)
                    group.save()
                    feature, created = Feature.objects.get_or_create(group=group, onec=spec['id'])
                    if created:
                        feature.name = feature_name
                        feature.is_filter = False
                        feature.is_primary = False
                        feature.widget_type = feature_type
                        feature.save()

                    value_product, created = FeatureValue.objects.get_or_create(product=product, onec=spec['value'], feature=feature)
                    if created:
                        value_product.value = feature_value
                        value_product.save()

    return


def parse_p(pxml):
    if not pxml.name:
        log_event('importing_catalog', u'Ошибка. у товара %s не указано имя. Данный товар не сохранён.' % pxml.pid,
                      'error')
    else:
        product = Product.objects.filter(onec = pxml.pid)
        if product:
            product = product[0]
            # log_event('importing_catalog', u'Товар %s найден'%(pxml.pid))

        else:
            product = Product()
            product.is_visible = False

            name_temp = slugify(pxml.name)
            # чек на повтор
            if check_used_slug(name_temp, Product):
                name_temp = '%s_%s' % (slugify(pxml.name), pxml.pid)
            product.slug = name_temp

            log_event('importing_catalog', u'Товар %s создан'%(pxml.pid))

        categ = Directory.objects.filter(onec=pxml.cat_id)
        if categ:
            categ = categ[0]
        else:
            categ,created = Directory.objects.get_or_create(name=u'!!!Без группы!!!')
            categ.is_visible = False
            categ.save()

        product.name = pxml.name
        product.directory = categ
        product.articul = pxml.articul
        product.description = pxml.description
        product.onecdir = pxml.cat_id
        product.onec = pxml.pid
        product.searchfield = u'%s %s %s %s' % (pxml.name, pxml.shid, pxml.sku, pxml.pid)
        product.save()
        parse_photos(pxml, product)
        parse_specs(pxml, product)
    return


# записываем товары
def xml_product(path_to_file):
    log_event('importing_catalog', u'Разбор товаров из XML файла')
    # try:
    for action, elem in etree.iterparse(path_to_file, tag=u'Товар'):
        if action == 'end':
            p = XmlProduct()
            propertys = []
            photos = []

            for e in elem.iterchildren():
                if e.tag == u'Ид':
                    p.pid = u'%s' % e.text

                if e.tag == u'Наименование':
                    p.name = u'%s' % e.text

                if e.tag == u'Группы':
                    for ep in e.iterchildren():
                        if ep.tag == u'Ид':
                            p.cat_id = u'%s' % ep.text

                if e.tag == u'Штрихкод':
                    p.shid = u'%s' % e.text

                if e.tag == u'Артикул':
                    p.articul = u'%s' % e.text

                if e.tag == u'Описание':
                    p.description = u'%s' % e.text

                if e.tag == u'Картинка':
                    photos.append(u'%s' % e.text)

                if e.tag == u'ЗначенияСвойств':
                    for ep in e.iterchildren():
                        prop = {}
                        for epp in ep.iterchildren():
                            if epp.tag == u'Ид':
                                prop['id'] = u'%s' % epp.text
                            if epp.tag == u'Значение':
                                prop['value'] = u'%s' % epp.text

                        propertys.append(prop)
            p.props = propertys
            p.photos = photos
            parse_p(p)
            elem.clear()

    # except Exception, e:
    #     log_event('importing_catalog', u'Критическая ошибка синтаксиса XML')
    #     log_event('importing_catalog', u'%s'%e,'critical_error')
    #     return
    return


def get_temp_file(source):
    xmlFile = os.path.join(settings.MEDIA_ROOT, 'uploads', 'data_exchange', source[source.rfind('/') + 1:])
    workFile = os.path.join(settings.MEDIA_ROOT, source[source.rfind('/') + 1:])
    shutil.copyfile(xmlFile, workFile)
    return workFile


def import_catalog():
    log_event('importing_catalog', u'Получаем путь до xml файла')
    dei = DataExchange.objects.get(type='importing_catalog')
    xmlFile = get_temp_file(dei.path)

    log_event('importing_catalog', u'Путь до XML файла %s' % xmlFile)

    if dei.ftp:
        ftp_ip = dei.ftp.ftp_ip
        ftp_login = dei.ftp.login
        ftp_pass = dei.ftp.passw
        xmlFileFTP = dei.path
        try:
            log_event('importing_catalog', u'Подключаемся к FTP')
            ftp = FTP(ftp_ip, ftp_login, ftp_pass, timeout=30)
            ftp.set_pasv(True)
        except:
            log_event('importing_catalog', u'Ошибка подключения к FTP', 'critical_error')
            return
        try:
            log_event('importing_catalog', u'Получаем XML файл')
            ftp.retrbinary('RETR %s' % xmlFileFTP, open(xmlFile, 'wb').write)
        except IOError:
            log_event('importing_catalog', u'Ошибка скачивания XML файла', 'critical_error')
            return
        try:
            ftp.quit()
        except:
            pass
    try:
        f = open(xmlFile, 'rb')
        f.close()
    except:
        log_event('importing_catalog', u'Ошибка. Невозможно открыть фаил %s' % xmlFile, 'critical_error')
        return

    log_event('importing_catalog', u'Заполняем разделы каталога')
    xml_to_catalog(xmlFile)  # заполняем разделы
    log_event('importing_catalog', u'Заполняем характеристики')
    xml_props_words(xmlFile)  # заполнение справочников характеристик
    log_event('importing_catalog', u'Заполняем товары')
    xml_product(xmlFile)  # заполнение продуктов и привязка их к разделам
    log_event('importing_catalog', u'Каталог успешно обновленн', 'success')
    return


def import_prices():
    log_event('importing_prices', u'Получение пути к XML файлу')
    dei = DataExchange.objects.get(type='importing_prices')
    xmlFile = get_temp_file(dei.path)
    log_event('importing_prices', u'Путь к XML файлу %s' % xmlFile)

    if dei.ftp:
        ftp_ip = dei.ftp.ftp_ip
        ftp_login = dei.ftp.login
        ftp_pass = dei.ftp.passw
        xmlFileFTP = dei.path
        try:
            log_event('importing_prices', u'Подключение к FTP')
            ftp = FTP(ftp_ip, ftp_login, ftp_pass, timeout=30)
            ftp.set_pasv(True)
        except:
            log_event('importing_prices', u'Ошибка. не удалось подключиться к FTP', 'critical_error')
            return
        try:
            log_event('importing_prices', u'Получение XML файла с  FTP')
            ftp.retrbinary('RETR %s' % xmlFileFTP, open(xmlFile, 'wb').write)
        except IOError:
            log_event('importing_prices', u'Ошибка. не удалось получить XML файл с FTP', 'critical_error')
            return
        ftp.quit()

    try:
        f = open(xmlFile, 'r')
        f.close()
    except:
        log_event('importing_prices', u'Ошибка. Невозможно открыть файл %s' % xmlFile, 'critical_error')
        return

    xml_to_sklads(xmlFile)
    log_event('importing_prices', u'Загрузка цен и остатков успешно завершена', 'success')
    return


# Загрузить каталог
def import_catalog_once():
    if log_event('importing_catalog', u'Старт импорта каталога', 'init'):
        return
    return import_catalog()


# Загрузить цены
def import_prices_once():
    if log_event('importing_prices', u'Старт импорта цен', 'init'):
        return
    return import_prices()


def clear_statuses_once():
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE %s' % DataExchangeLog._meta.db_table)
    return
