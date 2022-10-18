from rest_framework.routers import DefaultRouter

from apps.user_database.views import UserDatabaseViewSet, UserResourceViewSet

router = DefaultRouter()
router.register("user_database", UserDatabaseViewSet, basename="user_database")
router.register("user_resource", UserResourceViewSet, basename="user_resource")

urlpatterns = router.urls
