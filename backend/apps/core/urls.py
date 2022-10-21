from apps.core.views import FactionViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")

urlpatterns = [
    path("game_prices/", views.UserActionsViewSet.as_view())
] + router.urls
