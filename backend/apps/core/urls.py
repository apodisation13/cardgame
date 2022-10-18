# from django.urls import path
from apps.core.views import FactionViewSet  # , UserActionsApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")

# urlpatterns = [
#     path("game_prices/", UserActionsApiView.as_view())
# ] + router.urls

urlpatterns = router.urls
