"""
Tests for user admin configuration.
"""

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model

from users.admin import UserAdmin

User = get_user_model()


@pytest.mark.django_db
class TestUserAdmin:
    """Tests for UserAdmin configuration."""

    def test_user_admin_list_display(self):
        """Test UserAdmin list_display configuration."""
        admin = UserAdmin(User, AdminSite())

        expected_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "user_status",
            "is_staff"
        ]
        assert admin.list_display == expected_fields

    def test_user_admin_list_filter(self):
        """Test UserAdmin list_filter configuration."""
        admin = UserAdmin(User, AdminSite())

        expected_filters = [
            "is_staff",
            "is_superuser",
            "is_active",
            "user_status",
            "date_joined"
        ]
        assert admin.list_filter == expected_filters

    def test_user_admin_search_fields(self):
        """Test UserAdmin search_fields configuration."""
        admin = UserAdmin(User, AdminSite())

        expected_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone"
        ]
        assert admin.search_fields == expected_fields

    def test_user_admin_ordering(self):
        """Test UserAdmin ordering configuration."""
        admin = UserAdmin(User, AdminSite())

        assert admin.ordering == ["-date_joined"]

    def test_user_admin_fieldsets(self):
        """Test UserAdmin fieldsets configuration."""
        admin = UserAdmin(User, AdminSite())

        assert len(admin.fieldsets) == 5
        assert admin.fieldsets[0][1]["fields"] == ("username", "password")
        assert admin.fieldsets[2][0] == "Status"
        assert "user_status" in admin.fieldsets[2][1]["fields"]
