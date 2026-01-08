from django.contrib import admin
from django.urls import path

from myapp import views

# Admin branding
admin.site.site_header = "Pets Store Admin"
admin.site.site_title = "Pets Store Admin"
admin.site.index_title = "Store Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("pets/<int:pk>/", views.pet_detail, name="pet_detail"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
]
