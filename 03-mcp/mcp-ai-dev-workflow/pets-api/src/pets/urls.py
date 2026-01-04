"""
URL configuration for pets app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pets.views import CategoryViewSet, PetViewSet, TagViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"", PetViewSet, basename="pet")

urlpatterns = [
    path("", include(router.urls)),
]
