"""
Admin configuration for store app.
"""

from django.contrib import admin

from store.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""

    list_display = ["id", "pet", "user", "quantity", "status", "complete", "created_at"]
    list_filter = ["status", "complete", "created_at"]
    search_fields = ["pet__name", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    autocomplete_fields = ["pet", "user"]

    fieldsets = (
        ("Order Details", {
            "fields": ("pet", "user", "quantity")
        }),
        ("Status", {
            "fields": ("status", "complete", "ship_date")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
