from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import BronViewSet

router = DefaultRouter()
router.register('brons', BronViewSet, basename='brons')

urlpatterns = router.urls
