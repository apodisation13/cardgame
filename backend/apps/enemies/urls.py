from rest_framework.routers import DefaultRouter

from apps.enemies.views import EnemyLeaderViewSet, EnemyViewSet, LevelViewSet

router = DefaultRouter()
router.register("enemies", EnemyViewSet, basename="enemies")
router.register("levels", LevelViewSet, basename="levels")
router.register("enemy_leaders", EnemyLeaderViewSet, basename="enemy_leaders")

urlpatterns = router.urls
