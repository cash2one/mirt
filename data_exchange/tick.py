# -*- coding: utf-8 -*-
import os,sys
path = os.path.normpath(os.path.join(os.getcwd(), '..'))
sys.path.append(path)
path = os.path.normpath(os.getcwd())
sys.path.append(path)

from django.core.management import setup_environ
import main.settings

setup_environ(main.settings)

from data_exchange.tack import check_tick
check_tick()
