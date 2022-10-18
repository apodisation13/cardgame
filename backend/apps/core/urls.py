from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.views import FactionViewSet  # UserActionsApiView

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")

# urlpatterns = [
#     path("game_prices/", UserActionsApiView.as_view())
# ] + router.urls

urlpatterns = router.urls
