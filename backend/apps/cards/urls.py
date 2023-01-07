from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.cards.views import (
    CardViewSet,
    CraftUserCardViewSet,
    CraftUserLeaderViewSet,
    DeckViewSet,
    LeaderViewSet,
    MegaMillCardView,
    MillUserCardViewSet,
    MillUserLeaderViewSet,
    UserDeckViewSet,
)

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("decks", DeckViewSet, basename="decks")
router.register("leaders", LeaderViewSet, basename="leaders")
router.register("patchcards/craft_user_cards", CraftUserCardViewSet, basename="craft_user_cards")
router.register("patchcards/mill_user_cards", MillUserCardViewSet, basename="mill_user_cards")
router.register("patchleaders/craft_user_leaders", CraftUserLeaderViewSet, basename="craft_user_leaders")
router.register("patchleaders/mill_user_leaders", MillUserLeaderViewSet, basename="mill_user_leaders")
router.register("userdecks", UserDeckViewSet, basename="userdecks")

urlpatterns = [
    path("patchcards/mega_mill/", MegaMillCardView.as_view(), name='mega-mill'),
] + router.urls
