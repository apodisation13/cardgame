from rest_framework.routers import DefaultRouter

from apps.cards.views import CardViewSet, DeckViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("decks", DeckViewSet, basename="decks")


urlpatterns = router.urls
