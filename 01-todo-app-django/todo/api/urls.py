"""
API URL configuration for the TODO application.

This module defines the API routes using DRF's DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
