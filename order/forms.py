# -*- coding: utf-8 -*-

from order.models import Order, PAYMENT_TYPE
from django import forms


class OrderForm(forms.ModelForm):
    # payment_type = forms.ChoiceField(label=u'Способ оплаты', choices=PAYMENT_TYPE)
    class Meta:
        model = Order
        exclude = ('status', 'created_at')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label