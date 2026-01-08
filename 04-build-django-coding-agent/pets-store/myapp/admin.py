from django.contrib import admin

from .models import Pet, Product


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "pet_type", "breed", "age_years", "price", "in_stock", "created_at")
    list_filter = ("pet_type", "in_stock")
    search_fields = ("name", "breed", "description")
    ordering = ("-created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock", "created_at")
    list_filter = ("category", "in_stock")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
