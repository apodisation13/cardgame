from django.contrib import admin

from apps.news.models import News


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    model = News
    list_display_links = ('title', )
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'title', 'created_at', 'updated_at')
