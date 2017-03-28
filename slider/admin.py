# -*- coding: utf-8 -*-

from slider.models import Slide
from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE


class SliderForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE, label=u'Контент, располагаемый на слайде', required=False,)

    class Meta:
        model = Slide

class SlideAdmin(admin.ModelAdmin):
    form = SliderForm
    list_display = ('name', 'order', 'show',)
    list_editable = ('order', 'show')


admin.site.register(Slide, SlideAdmin)
