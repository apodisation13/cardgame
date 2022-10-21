from apps.news.views import NewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')

urlpatterns = router.urls
