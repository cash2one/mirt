# -*- coding: utf-8 -*-

from feedback.models import Feedback
from django.contrib import admin

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'name', 'phone', 'email', 'message', 'is_closed')
    list_editable = ('is_closed',)
    list_filter = ('created_at', 'is_closed', 'message',)
    list_display_links = ('id', 'created_at',)
    def has_add_permission(self, *args, **kwargs):
        return False

admin.site.register(Feedback, FeedbackAdmin)