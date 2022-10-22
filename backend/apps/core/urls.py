from rest_framework.routers import DefaultRouter

from apps.core.views import FactionViewSet, GameConstApiView

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")
router.register("game_const", GameConstApiView, basename="game_const")

urlpatterns = router.urls
