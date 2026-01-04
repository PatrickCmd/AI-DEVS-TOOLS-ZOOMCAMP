"""
Tests for user models.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            phone="1234567890",
            user_status=1
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.phone == "1234567890"
        assert user.user_status == 1
        assert user.check_password("testpass123")
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

        assert user.username == "admin"
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com"
        )

        assert str(user) == "testuser"

    def test_user_ordering(self):
        """Test that users are ordered by date_joined descending."""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")

        users = User.objects.all()
        assert users[0] == user2  # Most recent first
        assert users[1] == user1
