from rest_framework.routers import DefaultRouter

from apps.enemies.views import EnemyViewSet, LevelViewSet

router = DefaultRouter()
router.register("enemies", EnemyViewSet, basename="enemies")
router.register("levels", LevelViewSet, basename="levels")

urlpatterns = router.urls
