"""
URL configuration for Petstore API project.
"""

from django.contrib import admin
from django.urls import include, path

# Customize admin site
admin.site.site_header = "Pets Store Admin"
admin.site.site_title = "Pets Store Admin Portal"
admin.site.index_title = "Welcome to Pets Store Administration"
from drf_spectacular.views import (  # noqa: E402
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (  # noqa: E402
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # JWT Token endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # API v2 endpoints (matching OpenAPI spec paths)
    path("v2/pet/", include("pets.urls")),
    path("v2/store/", include("store.urls")),
    path("v2/user/", include("users.urls")),
]
