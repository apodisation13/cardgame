from apps.news.models import News
from django.contrib import admin


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    model = News
    list_display_links = ('title', )
    readonly_fields = ('created_at', )
    list_display = ('id', 'title', 'created_at')
