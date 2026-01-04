"""
Tests for pet models.
"""

import pytest
from django.db import IntegrityError

from pets.models import Category, Pet, Tag


@pytest.mark.django_db
class TestCategoryModel:
    """Tests for the Category model."""

    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(name="Dogs")

        assert category.name == "Dogs"
        assert str(category) == "Dogs"

    def test_category_repr(self):
        """Test category representation."""
        category = Category.objects.create(name="Cats")

        assert repr(category) == f"<Category Cats (id={category.id})>"

    def test_category_unique_name(self):
        """Test that category names must be unique."""
        Category.objects.create(name="Dogs")

        with pytest.raises(IntegrityError):
            Category.objects.create(name="Dogs")

    def test_category_ordering(self):
        """Test that categories are ordered by name."""
        cat_b = Category.objects.create(name="Birds")
        cat_a = Category.objects.create(name="Amphibians")
        cat_c = Category.objects.create(name="Cats")

        categories = Category.objects.all()
        assert categories[0] == cat_a
        assert categories[1] == cat_b
        assert categories[2] == cat_c


@pytest.mark.django_db
class TestTagModel:
    """Tests for the Tag model."""

    def test_create_tag(self):
        """Test creating a tag."""
        tag = Tag.objects.create(name="friendly")

        assert tag.name == "friendly"
        assert str(tag) == "friendly"

    def test_tag_repr(self):
        """Test tag representation."""
        tag = Tag.objects.create(name="cute")

        assert repr(tag) == f"<Tag cute (id={tag.id})>"

    def test_tag_unique_name(self):
        """Test that tag names must be unique."""
        Tag.objects.create(name="playful")

        with pytest.raises(IntegrityError):
            Tag.objects.create(name="playful")

    def test_tag_ordering(self):
        """Test that tags are ordered by name."""
        tag_c = Tag.objects.create(name="calm")
        tag_a = Tag.objects.create(name="active")
        tag_b = Tag.objects.create(name="brave")

        tags = Tag.objects.all()
        assert tags[0] == tag_a
        assert tags[1] == tag_b
        assert tags[2] == tag_c


@pytest.mark.django_db
class TestPetModel:
    """Tests for the Pet model."""

    def test_create_pet(self, category):
        """Test creating a pet."""
        pet = Pet.objects.create(
            name="Fluffy",
            category=category,
            status="available",
            photo_urls=["http://example.com/fluffy.jpg"]
        )

        assert pet.name == "Fluffy"
        assert pet.category == category
        assert pet.status == "available"
        assert len(pet.photo_urls) == 1

    def test_pet_str_representation(self, category):
        """Test pet string representation."""
        pet = Pet.objects.create(
            name="Max",
            category=category,
            status="available"
        )

        assert str(pet) == "Max (Available)"

    def test_pet_repr(self, category):
        """Test pet representation."""
        pet = Pet.objects.create(
            name="Buddy",
            category=category,
            status="sold"
        )

        assert repr(pet) == f"<Pet Buddy (id={pet.id}, status=sold)>"

    def test_pet_with_tags(self, category):
        """Test creating a pet with tags."""
        tag1 = Tag.objects.create(name="friendly")
        tag2 = Tag.objects.create(name="playful")

        pet = Pet.objects.create(
            name="Charlie",
            category=category,
            status="available"
        )
        pet.tags.add(tag1, tag2)

        assert pet.tags.count() == 2
        assert tag1 in pet.tags.all()
        assert tag2 in pet.tags.all()

    def test_pet_default_status(self, category):
        """Test pet default status is 'available'."""
        pet = Pet.objects.create(
            name="Rex",
            category=category
        )

        assert pet.status == "available"

    def test_pet_status_choices(self):
        """Test pet status choices."""
        assert Pet.Status.AVAILABLE == "available"
        assert Pet.Status.PENDING == "pending"
        assert Pet.Status.SOLD == "sold"

    def test_pet_ordering(self, category):
        """Test that pets are ordered by created_at descending."""
        pet1 = Pet.objects.create(name="Pet1", category=category)
        pet2 = Pet.objects.create(name="Pet2", category=category)

        pets = Pet.objects.all()
        assert pets[0] == pet2  # Most recent first
        assert pets[1] == pet1

    def test_pet_without_category(self):
        """Test creating a pet without category."""
        pet = Pet.objects.create(
            name="Stray",
            status="available"
        )

        assert pet.category is None
        assert pet.name == "Stray"
