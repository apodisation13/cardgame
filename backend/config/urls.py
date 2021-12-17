from django.contrib import admin
from django.urls import include, path

from config.api_docs import urlpatterns as api_docs_urlpatterns

urlpatterns = api_docs_urlpatterns + [
    path('admin/', admin.site.urls),
    path('api/v1/', include("apps.cards.urls"))
]
