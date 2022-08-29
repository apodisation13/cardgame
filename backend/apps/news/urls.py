from rest_framework.routers import DefaultRouter

from apps.news.views import NewsViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')

urlpatterns = router.urls
