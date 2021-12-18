from rest_framework.routers import DefaultRouter

from apps.cards.views import CardViewSet, TryViewSet, DeckViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("try", TryViewSet, basename="try")
router.register("decks", DeckViewSet, basename="decks")


urlpatterns = router.urls
