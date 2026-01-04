"""
Admin configuration for users app.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""

    list_display = ["username", "email", "first_name", "last_name", "phone", "user_status", "is_staff"]
    list_filter = ["is_staff", "is_superuser", "is_active", "user_status", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name", "phone"]
    ordering = ["-date_joined"]

    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "email", "phone")
        }),
        ("Status", {
            "fields": ("user_status",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "phone", "user_status"),
        }),
    )
