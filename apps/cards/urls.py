from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("catalog", CatalogViewSet, basename="catalog")


urlpatterns = router.urls
