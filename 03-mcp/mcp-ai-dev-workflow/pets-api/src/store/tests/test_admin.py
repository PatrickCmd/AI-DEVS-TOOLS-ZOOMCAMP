"""
Tests for store admin configuration.
"""

import pytest
from django.contrib.admin.sites import AdminSite

from store.admin import OrderAdmin
from store.models import Order


@pytest.mark.django_db
class TestOrderAdmin:
    """Tests for OrderAdmin configuration."""

    def test_order_admin_list_display(self):
        """Test OrderAdmin list_display configuration."""
        admin = OrderAdmin(Order, AdminSite())

        expected_fields = [
            "id",
            "pet",
            "user",
            "quantity",
            "status",
            "complete",
            "created_at"
        ]
        assert admin.list_display == expected_fields

    def test_order_admin_list_filter(self):
        """Test OrderAdmin list_filter configuration."""
        admin = OrderAdmin(Order, AdminSite())

        expected_filters = ["status", "complete", "created_at"]
        assert admin.list_filter == expected_filters

    def test_order_admin_search_fields(self):
        """Test OrderAdmin search_fields configuration."""
        admin = OrderAdmin(Order, AdminSite())

        expected_fields = ["pet__name", "user__username"]
        assert admin.search_fields == expected_fields

    def test_order_admin_readonly_fields(self):
        """Test OrderAdmin readonly_fields configuration."""
        admin = OrderAdmin(Order, AdminSite())

        assert admin.readonly_fields == ["created_at", "updated_at"]

    def test_order_admin_ordering(self):
        """Test OrderAdmin ordering configuration."""
        admin = OrderAdmin(Order, AdminSite())

        assert admin.ordering == ["-created_at"]

    def test_order_admin_autocomplete_fields(self):
        """Test OrderAdmin autocomplete_fields configuration."""
        admin = OrderAdmin(Order, AdminSite())

        assert admin.autocomplete_fields == ["pet", "user"]

    def test_order_admin_fieldsets(self):
        """Test OrderAdmin fieldsets configuration."""
        admin = OrderAdmin(Order, AdminSite())

        assert len(admin.fieldsets) == 3
        assert admin.fieldsets[0][0] == "Order Details"
        assert admin.fieldsets[1][0] == "Status"
        assert admin.fieldsets[2][0] == "Timestamps"
