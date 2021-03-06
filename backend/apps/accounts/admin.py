from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import CustomUser
from apps.cards.models import UserCard


class UserCardInLine(admin.TabularInline):
    model = UserCard


class CustomUserAdmin(UserAdmin):
    inlines = [UserCardInLine, ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
