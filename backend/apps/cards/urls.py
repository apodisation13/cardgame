from rest_framework.routers import DefaultRouter

from apps.cards.views import CardViewSet, DeckViewSet, LeaderViewSet, UserDatabaseViewSet

router = DefaultRouter()
router.register("cards", CardViewSet, basename="cards")
router.register("decks", DeckViewSet, basename="decks")
router.register("leaders", LeaderViewSet, basename="leaders")
router.register("user_database", UserDatabaseViewSet, basename="user_database")


urlpatterns = router.urls
