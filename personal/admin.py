# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from personal.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    list_display = ('pk','get_user','email','first_name','last_name','get_mobile','date_joined','is_staff')
    inlines = (UserProfileInline,)

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        if not request.user.is_superuser:
            permissions = ['auth.add_user', 'auth.change_user', 'auth.delete_user']
            for perm in request.user.get_all_permissions():
                if perm in permissions:
                    return qs.filter(is_superuser=False, is_staff=False)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user)

    def get_user(self, obj):
        return obj.username
    get_user.short_description = u'Логин пользователя'
    get_user.admin_order_field = 'username'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return super(UserAdmin, self).get_fieldsets(request, obj)
        else:
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'email')}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff', 'user_permissions')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                (_('Groups'), {'fields': ('groups',)}),
                )

        return fieldsets

    def get_mobile(self, obj):
        return UserProfile.objects.get(user=obj).phone
    get_mobile.short_description = u"Мобильный телефон"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)