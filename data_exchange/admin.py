# -*- coding: utf-8 -*-
from django.contrib import admin
from data_exchange.models import DataExchange, ExchangeFTPs, DataExchangeLog, RunSchedule
from django.db import connection
from django.contrib import messages
for_start = True # Настройка для включения добавления(True - добавление включено)


class TimeInline(admin.TabularInline):
    model = RunSchedule
    fk_name = "data"
    extra = 0

class DataExchangeAdmin(admin.ModelAdmin):
    list_display = ('type', 'ftp', 'path', 'busy', 'time_start', 'time_finish',)#'state', 'date_done')
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('type', 'ftp', 'path', 'busy', 'time_start', 'time_finish')
        }),
    )
    inlines = [TimeInline,]
    #actions = [start_data_exchange,]


    def has_add_permission(self, *args, **kwargs):
        return for_start


    def has_delete_permission(self, request, obj=None):
        return for_start

admin.site.register(DataExchange, DataExchangeAdmin)


class ExchangeFTPsAdmin(admin.ModelAdmin):
    list_display = ('ftp_ip', 'login', 'name')
    list_editable = ('name',)

admin.site.register(ExchangeFTPs,ExchangeFTPsAdmin)


def clear_all(modeladmin, request, queryset):
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE {0}'.format(DataExchangeLog._meta.db_table))
    messages.success(request, u'Лог успешно очищен')

clear_all.short_description = u'Очистить все'


class DLogAdmin(admin.ModelAdmin):
    list_display = ('data', 'time_start', 'message',)
    readonly_fields = ('data', 'time_start',)
    search_fields = ('message',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    actions = (clear_all,)

admin.site.register(DataExchangeLog, DLogAdmin)