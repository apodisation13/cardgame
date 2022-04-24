from rest_framework.routers import DefaultRouter

from apps.user_database.views import UserDatabaseViewSet

router = DefaultRouter()
router.register("user_database", UserDatabaseViewSet, basename="user_database")

urlpatterns = router.urls
