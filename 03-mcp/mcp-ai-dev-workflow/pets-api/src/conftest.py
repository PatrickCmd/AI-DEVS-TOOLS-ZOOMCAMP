"""
Pytest configuration and fixtures for Petstore API tests.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from pets.models import Category, Pet, Tag
from store.models import Order

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone="1234567890"
    )


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123"
    )


@pytest.fixture
def user_tokens(user):
    """Generate JWT tokens for the test user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@pytest.fixture
def authenticated_client(api_client, user_tokens):
    """Return an authenticated API client."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
    return api_client


@pytest.fixture
def category(db):
    """Create and return a test category."""
    return Category.objects.create(name="Dogs")


@pytest.fixture
def tag(db):
    """Create and return a test tag."""
    return Tag.objects.create(name="friendly")


@pytest.fixture
def pet(db, category, tag):
    """Create and return a test pet."""
    pet = Pet.objects.create(
        name="Fluffy",
        category=category,
        status="available",
        photo_urls=["http://example.com/fluffy.jpg"]
    )
    pet.tags.add(tag)
    return pet


@pytest.fixture
def order(db, pet, user):
    """Create and return a test order."""
    return Order.objects.create(
        pet=pet,
        user=user,
        quantity=1,
        status="placed"
    )
