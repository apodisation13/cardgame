from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('news', NewsView, basename='news')

urlpatterns = router.urls