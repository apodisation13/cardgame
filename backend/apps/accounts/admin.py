from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import CustomUser
from apps.cards.models import UserCard, UserLeader
from apps.enemies.models import UserLevel


class UserCardInLine(admin.TabularInline):
    model = UserCard
    extra = 0


class LevelInline(admin.TabularInline):
    model = UserLevel
    extra = 0


class LeaderInline(admin.TabularInline):
    model = UserLeader
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [UserCardInLine, LeaderInline, LevelInline, ]
    fieldsets = UserAdmin.fieldsets + (
        ('Resources', {'fields': ('scraps', 'wood', 'kegs', 'big_kegs', 'chests', 'keys')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
