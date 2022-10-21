from apps.enemies.views import (EnemyLeaderViewSet, EnemyViewSet, LevelViewSet,
                                UnlockLevelsViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("enemies", EnemyViewSet, basename="enemies")
router.register("levels", LevelViewSet, basename="levels")
router.register("enemy_leaders", EnemyLeaderViewSet, basename="enemy_leaders")
router.register("unlock_levels", UnlockLevelsViewSet, basename="unlock_levels")

urlpatterns = router.urls
