# -*- coding: utf-8 -*-

import os
import sys
import datetime

path = os.path.normpath(os.path.join(os.getcwd(), '..'))
sys.path.append(path)
from django.core.management import setup_environ
import main.settings

setup_environ(main.settings)

from catalog.filter_widget import FilterWidget
from catalog.models import Directory, Brand, Product, Image, ImageManager

# os.system('clear')

# FilterWidget - это конструктор виджета фильтра по характеристикам
# суть в том, что имея дополнительный слой абстракции, мы сможем менять модели характеристик
# при этом не меняя фронтенд

# Теперь объяснялки, чё тут кого )
test_start = datetime.datetime.now()

url = "/"
widget = FilterWidget(url)  # создаём экземпляр виджета, url - это будет action у формы

# как добавить характеристики?

# важно - для любого виджета нада указать name и type,
# ещё для любого виджета есть label - название, которое будет выводиться на шаблоне,
# оно опционально, если не указать, то продублируется name

# type возможны такие : fader_double, select_box, checkbox


# fader_double... ну или штука с двумя ползунками=)
widget.update_feature(name="example fader",
                      type="fader_double",
                      label=u"пример штуки с ползунками",
                      min=100, max=500,  # ну тут понятно - пределбные значения для ползунков
                      current_min=133, current_max=455)  # - текущие значения ползунков, по-умолчанию равны min и max


# select_box - всеми любимый выпадающий списочег
# Пример 1 - когда значения характеристик совпадают с именами
widget.update_feature(name="example select 1",
                      type="select_box",
                      label=u"списочек 1",
                      order=1,  # по-умолчанию order = 0
                      values=[1, 2, 3],  # списк значений
                      selected_values=[2],  # списк выбранных, если не казать, то, типа, ничиго не выбрано
                      )

# Пример 2 - когда значения характеристик - это, допустим, их айдишники в базе, а названия... что-нить на русском
# Возьмём модельку брендов
widget.update_feature(name="example select 2",
                      type="select_box",
                      label=u"списочек 2",
                      order=2,
                      with_labels=True,  # нада добаить этот параметр, чтобы
                      values=Brand.objects.all().values_list("id", "name"),  # Вот тут важен порядок!
                      # сначала значения, потом названия
                      selected_values=map(long, ["1"]),  # соответственно, в выбранные значения заносим айдишники
                      )

# checkbox - галочка в квадратике такая, тут всё много проще
widget.update_feature(name="example checkbox",
                      label=u"Галочка, типа",
                      type="checkbox",
                      order=3,
                      checked=True)  # если чекбокс не выбран, то параметр можно опустить


# и ещё - на всякий случай напоминаю, что именованные аргументы можно отправлять словарём,
# возможно, в некоторых случаях, это будет единственный способ составить набор необходимых аргументов

# составляем словарь
values_dict = {"name": "example select from dict",
               "type": "select_box",
               "label": u"пример селекта, составленного из словаря",
               "values": ["Kill", "them", "all!"],
               "selected_values": ["Kill"],
               "order": 4}


# теперь, чтобы отправить словарь как именованные аргументы, нужно дорисовать **
widget.update_feature(**values_dict)


# проверяем, что получилось
test_end = datetime.datetime.now()
test_time = test_end - test_start

test_file = open("filter_widget_test_output.txt", 'w')

for item in widget.get_features():

    test_file.write("name: %s\n  type: %s\n  values: %s\n\n" % (item.name, item.widget, vars(item.widget)))

test_file.write("test time: %s\n" % test_time)
test_file.close()
print "done!"