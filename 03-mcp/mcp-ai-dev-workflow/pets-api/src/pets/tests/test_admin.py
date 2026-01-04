"""
Tests for pet admin configuration.
"""

import pytest
from django.contrib.admin.sites import AdminSite

from pets.admin import CategoryAdmin, PetAdmin, TagAdmin
from pets.models import Category, Pet, Tag


@pytest.mark.django_db
class TestCategoryAdmin:
    """Tests for CategoryAdmin configuration."""

    def test_category_admin_list_display(self):
        """Test CategoryAdmin list_display configuration."""
        admin = CategoryAdmin(Category, AdminSite())

        assert admin.list_display == ["id", "name"]

    def test_category_admin_search_fields(self):
        """Test CategoryAdmin search_fields configuration."""
        admin = CategoryAdmin(Category, AdminSite())

        assert admin.search_fields == ["name"]

    def test_category_admin_ordering(self):
        """Test CategoryAdmin ordering configuration."""
        admin = CategoryAdmin(Category, AdminSite())

        assert admin.ordering == ["name"]


@pytest.mark.django_db
class TestTagAdmin:
    """Tests for TagAdmin configuration."""

    def test_tag_admin_list_display(self):
        """Test TagAdmin list_display configuration."""
        admin = TagAdmin(Tag, AdminSite())

        assert admin.list_display == ["id", "name"]

    def test_tag_admin_search_fields(self):
        """Test TagAdmin search_fields configuration."""
        admin = TagAdmin(Tag, AdminSite())

        assert admin.search_fields == ["name"]

    def test_tag_admin_ordering(self):
        """Test TagAdmin ordering configuration."""
        admin = TagAdmin(Tag, AdminSite())

        assert admin.ordering == ["name"]


@pytest.mark.django_db
class TestPetAdmin:
    """Tests for PetAdmin configuration."""

    def test_pet_admin_list_display(self):
        """Test PetAdmin list_display configuration."""
        admin = PetAdmin(Pet, AdminSite())

        expected_fields = ["id", "name", "category", "status", "created_at"]
        assert admin.list_display == expected_fields

    def test_pet_admin_list_filter(self):
        """Test PetAdmin list_filter configuration."""
        admin = PetAdmin(Pet, AdminSite())

        expected_filters = ["status", "category", "created_at"]
        assert admin.list_filter == expected_filters

    def test_pet_admin_search_fields(self):
        """Test PetAdmin search_fields configuration."""
        admin = PetAdmin(Pet, AdminSite())

        expected_fields = ["name", "tags__name"]
        assert admin.search_fields == expected_fields

    def test_pet_admin_filter_horizontal(self):
        """Test PetAdmin filter_horizontal configuration."""
        admin = PetAdmin(Pet, AdminSite())

        assert admin.filter_horizontal == ["tags"]

    def test_pet_admin_readonly_fields(self):
        """Test PetAdmin readonly_fields configuration."""
        admin = PetAdmin(Pet, AdminSite())

        assert admin.readonly_fields == ["created_at", "updated_at"]

    def test_pet_admin_fieldsets(self):
        """Test PetAdmin fieldsets configuration."""
        admin = PetAdmin(Pet, AdminSite())

        assert len(admin.fieldsets) == 4
        assert admin.fieldsets[0][0] == "Basic Information"
        assert admin.fieldsets[1][0] == "Media"
        assert admin.fieldsets[2][0] == "Tags"
        assert admin.fieldsets[3][0] == "Timestamps"
