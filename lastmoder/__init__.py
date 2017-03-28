# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.admin.models import LogEntry
from email.utils import formatdate
import time


def datetime2rfc(dt):
    dt = time.mktime(dt.timetuple())
    return formatdate(dt, usegmt=True)


def get_last_time():
    try:
        last_log = LogEntry.objects.order_by('-pk')[0]
        return datetime2rfc(last_log.action_time)
    except:
        return datetime.now()