from rest_framework.routers import DefaultRouter

from apps.cards.views import CardViewSet, DeckViewSet, LeaderViewSet, UserCardsViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("decks", DeckViewSet, basename="decks")
router.register("leaders", LeaderViewSet, basename="leaders")
router.register("usercards", UserCardsViewSet, basename="usercards")


urlpatterns = router.urls
