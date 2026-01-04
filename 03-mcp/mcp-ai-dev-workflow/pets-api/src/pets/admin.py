"""
Admin configuration for pets app.
"""

from django.contrib import admin

from pets.models import Category, Pet, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model."""

    list_display = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Admin configuration for Pet model."""

    list_display = ["id", "name", "category", "status", "created_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["name", "tags__name"]
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "category", "status")
        }),
        ("Media", {
            "fields": ("photo_urls",)
        }),
        ("Tags", {
            "fields": ("tags",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
