# -*- coding: utf-8 -*-
from datetime import datetime
from data_exchange.models import RunSchedule,DataExchange
from data_exchange.views import import_prices_once, import_catalog_once

def check_tick():
    current_time = datetime.now()
    hour = int(current_time.strftime("%H"))
    min = int(current_time.strftime("%M"))
    print hour,min
    data_for_run = []
    objs = RunSchedule.objects.filter(hours__isnull=True, min=min,active=True).values_list('data',flat=True)
    for f in objs:
        if f not in data_for_run:
            data_for_run.append(f)

    objs = RunSchedule.objects.filter(hours=hour, min=min,active=True).values_list('data',flat=True)
    for f in objs:
        if f not in data_for_run:
            data_for_run.append(f)

    objs = RunSchedule.objects.filter(hours=hour, min__isnull=True,active=True).values_list('data',flat=True)
    for f in objs:
        if f not in data_for_run:
            data_for_run.append(f)

    objs = RunSchedule.objects.filter(hours__isnull=True, min__isnull=True,active=True).values_list('data',flat=True)
    for f in objs:
        if f not in data_for_run:
            data_for_run.append(f)
    print data_for_run
    for data_ex in data_for_run:
        data = DataExchange.objects.get(id=data_ex)
        if data.type == 'importing_catalog':
            print 'load catalog'
            import_catalog_once()
        elif data.type == 'importing_prices':
            print 'load price'
            import_prices_once()



