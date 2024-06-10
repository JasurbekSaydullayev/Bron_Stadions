from django.urls import path

from rest_framework.routers import DefaultRouter

from stadions.api.views import StadionViewSet, PhotoViewSet

router = DefaultRouter()
router.register('stadions', StadionViewSet, basename='stadions')
router.register('photos', PhotoViewSet, basename='photos')

urlpatterns = router.urls
