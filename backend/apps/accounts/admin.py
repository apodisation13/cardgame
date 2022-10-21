from apps.accounts.models import CustomUser
from apps.cards.models import UserCard
from apps.enemies.models import UserLevel
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserCardInLine(admin.TabularInline):
    model = UserCard


class LevelInline(admin.TabularInline):
    model = UserLevel


class CustomUserAdmin(UserAdmin):
    inlines = [UserCardInLine, LevelInline, ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
