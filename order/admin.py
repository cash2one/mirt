# -*- coding: utf-8 -*-

from django.contrib import admin
from order.models import Order, OrderItem, OrderStatus


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_initial', 'is_closing', 'index_number')
    list_editable = ('is_initial', 'is_closing', 'index_number')
    list_filter = ('is_initial',)

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'is_initial', 'is_closing', 'index_number',)
        }),
        )

admin.site.register(OrderStatus, OrderStatusAdmin)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


admin.site.register(OrderItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'order_items', 'full_name', 'phone', 'total_price', 'status')
    list_editable = ('status',)
    list_filter = ('created_at', 'status')
    inlines = (OrderItemInline,)

    fieldsets = (
#        (u'Пользователь', {
#            'classes': ('collapse',),
#            'fields': ('user',)
#        }),
        (u'Информация о покупателе', {
            'classes': ('collapse',),
            'fields': ('full_name', 'phone', 'email')
        }),
        (u'Доставка', {
            'classes': ('collapse',),
            'fields': ('city', 'postal_code', 'address','street','house','apartment', ),
            }),

        (u'Оплата', {
            'classes': ('collapse',),
            'fields': ('payment_type',),
            }),
        (u'Магазины', {
            'classes': ('collapse',),
            'fields': ('webstock',),
            }),

        (u'Статус', {
            'classes': ('collapse',),
            'fields': ('status',),
            }),
        # (u'Дополнительная информация', {
        #     'classes': ('collapse',),
        #     'fields': ('external_id',),
        #     }),
        (u'Комментарий к заказу', {
            'classes': ('collapse',),
            'fields': ('comment',)
        }),
        )

    def has_add_permission(self, *args, **kwargs):
        return False

    def order_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        try:
            return ', '.join([ "<a href='%s' target='_blank'>%s</a>" % (
                item.product.get_absolute_url(), item.product.name
                ) for item in items ])
        except:
            return ''

    order_items.short_description = u'Список товаров'
    order_items.allow_tags = True

    def total_price(self, obj):
        items = OrderItem.objects.filter(order=obj)
        summary = 0
        for item in items:
            summary += item.price * item.quantity
        return str(int(summary))
    total_price.short_description = u'Итоговая цена'

admin.site.register(Order, OrderAdmin)