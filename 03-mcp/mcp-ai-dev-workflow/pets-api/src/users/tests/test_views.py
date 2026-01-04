"""
Tests for user views and endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Tests for user registration endpoint."""

    def test_create_user_success(self, api_client):
        """Test creating a new user successfully."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User"
        }
        response = api_client.post("/v2/user/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["username"] == "newuser"
        assert User.objects.filter(username="newuser").exists()

    def test_create_user_missing_required_fields(self, api_client):
        """Test creating user with missing required fields."""
        data = {"username": "newuser"}
        response = api_client.post("/v2/user/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_duplicate_username(self, api_client, user):
        """Test creating user with duplicate username."""
        data = {
            "username": "testuser",  # Already exists
            "email": "another@example.com",
            "password": "pass123"
        }
        response = api_client.post("/v2/user/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_success(self, api_client, user):
        """Test successful login."""
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = api_client.post("/v2/user/login/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials."""
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = api_client.post("/v2/user/login/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with nonexistent user."""
        data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = api_client.post("/v2/user/login/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserRetrieve:
    """Tests for retrieving user information."""

    def test_get_user_by_username(self, authenticated_client, user):
        """Test retrieving user by username."""
        response = authenticated_client.get(f"/v2/user/{user.username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_get_user_unauthenticated(self, api_client, user):
        """Test retrieving user without authentication."""
        response = api_client.get(f"/v2/user/{user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_nonexistent_user(self, authenticated_client):
        """Test retrieving nonexistent user."""
        response = authenticated_client.get("/v2/user/nonexistent/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUserUpdate:
    """Tests for updating user information."""

    def test_update_own_profile(self, authenticated_client, user):
        """Test updating own profile."""
        data = {
            "first_name": "Updated",
            "phone": "9876543210"
        }
        response = authenticated_client.patch(
            f"/v2/user/{user.username}/",
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["phone"] == "9876543210"

    def test_update_other_user_profile(self, authenticated_client, admin_user):
        """Test updating another user's profile (should fail)."""
        data = {"first_name": "Hacked"}
        response = authenticated_client.patch(
            f"/v2/user/{admin_user.username}/",
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserDelete:
    """Tests for deleting user account."""

    def test_delete_own_account(self, authenticated_client, user):
        """Test deleting own account."""
        response = authenticated_client.delete(f"/v2/user/{user.username}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(username=user.username).exists()

    def test_delete_other_user_account(self, authenticated_client, admin_user):
        """Test deleting another user's account (should fail)."""
        response = authenticated_client.delete(f"/v2/user/{admin_user.username}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserLogout:
    """Tests for user logout."""

    def test_logout_success(self, authenticated_client, user_tokens):
        """Test successful logout."""
        data = {"refresh": user_tokens["refresh"]}
        response = authenticated_client.post("/v2/user/logout/", data, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_logout_missing_refresh_token(self, authenticated_client):
        """Test logout without refresh token."""
        response = authenticated_client.post("/v2/user/logout/", {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserMe:
    """Tests for /user/me endpoint."""

    def test_get_current_user_success(self, authenticated_client, user):
        """Test getting current user's profile."""
        response = authenticated_client.get("/v2/user/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name

    def test_get_current_user_unauthenticated(self, api_client):
        """Test accessing /user/me without authentication."""
        response = api_client.get("/v2/user/me/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_returns_full_profile(self, authenticated_client, user):
        """Test that /user/me returns all expected user fields."""
        response = authenticated_client.get("/v2/user/me/")

        assert response.status_code == status.HTTP_200_OK

        # Check all expected fields are present
        expected_fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "user_status"
        ]
        for field in expected_fields:
            assert field in response.data

    def test_get_current_user_with_updated_profile(self, authenticated_client, user):
        """Test that /user/me reflects updated user information."""
        # Update user
        user.first_name = "Updated"
        user.last_name = "Name"
        user.phone = "9876543210"
        user.save()

        response = authenticated_client.get("/v2/user/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"
        assert response.data["phone"] == "9876543210"

    def test_get_current_user_password_not_included(self, authenticated_client):
        """Test that password is not included in /user/me response."""
        response = authenticated_client.get("/v2/user/me/")

        assert response.status_code == status.HTTP_200_OK
        assert "password" not in response.data

    def test_get_current_user_different_authenticated_users(self, api_client):
        """Test that different authenticated users get their own profile."""
        # Create two users
        user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="pass123"
        )
        user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass123"
        )

        # Login as user1
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh1 = RefreshToken.for_user(user1)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh1.access_token}')

        response1 = api_client.get("/v2/user/me/")
        assert response1.status_code == status.HTTP_200_OK
        assert response1.data["username"] == "user1"

        # Login as user2
        refresh2 = RefreshToken.for_user(user2)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh2.access_token}')

        response2 = api_client.get("/v2/user/me/")
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data["username"] == "user2"

    def test_get_current_user_method_not_allowed(self, authenticated_client):
        """Test that only GET method is allowed on /user/me."""
        # Test POST
        response = authenticated_client.post("/v2/user/me/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        # Test PUT
        response = authenticated_client.put("/v2/user/me/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        # Test DELETE
        response = authenticated_client.delete("/v2/user/me/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
