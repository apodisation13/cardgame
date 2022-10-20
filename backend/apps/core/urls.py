from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.views import FactionViewSet, GameConstApiView

router = DefaultRouter()
router.register("factions", FactionViewSet, basename="factions")

urlpatterns = [
    path("game_const/", GameConstApiView.as_view())
] + router.urls
