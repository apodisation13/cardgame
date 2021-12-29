from rest_framework.routers import DefaultRouter

from apps.cards.views import CardViewSet, DeckViewSet, FactionViewSet, LeaderViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("decks", DeckViewSet, basename="decks")
router.register("factions", FactionViewSet, basename="factions")
router.register("leaders", LeaderViewSet, basename="leaders")


urlpatterns = router.urls
