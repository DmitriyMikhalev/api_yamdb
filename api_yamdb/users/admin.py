from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'bio',)
        }),
        ('Права', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
                'groups',
                'user_permissions',
            )
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role',
        'id',
    )
    list_editable = (
        'role',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'username',
    )
    ordering = ('email', 'first_name', '-id', 'last_name', 'username',)


admin.site.register(User, UserAdminCustom)
