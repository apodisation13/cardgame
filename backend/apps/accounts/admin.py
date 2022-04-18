from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
