from rest_framework.routers import DefaultRouter

from apps.core.views import FactionViewSet

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")


urlpatterns = router.urls
