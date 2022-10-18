from apps.accounts.views import CreateUserViewSet, LoginViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("register", CreateUserViewSet, basename="register")
router.register("login", LoginViewSet, basename="login")


urlpatterns = router.urls
