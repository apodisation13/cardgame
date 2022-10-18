from apps.user_database.views import UserDatabaseViewSet, UserResourceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("user_database", UserDatabaseViewSet, basename="user_database")
router.register("user_resource", UserResourceViewSet, basename="user_resource")

urlpatterns = router.urls
