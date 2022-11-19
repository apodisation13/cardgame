from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.accounts.views import CustomAuthToken
from config.api_docs import urlpatterns as api_docs_urlpatterns

urlpatterns = api_docs_urlpatterns + [
    path('admin/', admin.site.urls),
    path('api/v1/', include("apps.core.urls")),
    path('api/v1/', include("apps.cards.urls")),
    path('api/v1/', include("apps.enemies.urls")),
    path('accounts/', include("apps.accounts.urls")),
    path('api/v1/', include("apps.user_database.urls")),
    path('accounts/api-token-auth/', CustomAuthToken.as_view()),
    path('api/v1/', include("apps.news.urls")),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
