"""
Tests for pet views and endpoints.
"""

import pytest
from rest_framework import status

from pets.models import Category, Pet, Tag


@pytest.mark.django_db
class TestPetCreate:
    """Tests for creating pets."""

    def test_create_pet_authenticated(self, authenticated_client):
        """Test creating a pet with authentication."""
        data = {
            "name": "Max",
            "status": "available",
            "photo_urls": ["http://example.com/max.jpg"]
        }
        response = authenticated_client.post("/v2/pet/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Max"
        assert Pet.objects.filter(name="Max").exists()

    def test_create_pet_unauthenticated(self, api_client):
        """Test creating a pet without authentication."""
        data = {
            "name": "Max",
            "status": "available"
        }
        response = api_client.post("/v2/pet/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_pet_with_category_and_tags(self, authenticated_client, category, tag):
        """Test creating a pet with category and tags."""
        data = {
            "name": "Buddy",
            "status": "available",
            "photo_urls": [],
            "category_id": category.id,
            "tag_ids": [tag.id]
        }
        response = authenticated_client.post("/v2/pet/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["category"]["id"] == category.id
        assert len(response.data["tags"]) == 1


@pytest.mark.django_db
class TestPetList:
    """Tests for listing pets."""

    def test_list_pets(self, api_client, pet):
        """Test listing all pets."""
        response = api_client.get("/v2/pet/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_list_pets_pagination(self, api_client, pet):
        """Test pet list pagination."""
        response = api_client.get("/v2/pet/")

        assert "results" in response.data
        assert "count" in response.data


@pytest.mark.django_db
class TestPetRetrieve:
    """Tests for retrieving a single pet."""

    def test_get_pet_by_id(self, api_client, pet):
        """Test retrieving a pet by ID."""
        response = api_client.get(f"/v2/pet/{pet.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == pet.name
        assert response.data["status"] == pet.status

    def test_get_nonexistent_pet(self, api_client):
        """Test retrieving a nonexistent pet."""
        response = api_client.get("/v2/pet/99999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPetUpdate:
    """Tests for updating pets."""

    def test_update_pet(self, authenticated_client, pet):
        """Test updating a pet."""
        data = {
            "name": "Fluffy Updated",
            "status": "sold"
        }
        response = authenticated_client.patch(
            f"/v2/pet/{pet.id}/",
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Fluffy Updated"
        assert response.data["status"] == "sold"

    def test_update_pet_unauthenticated(self, api_client, pet):
        """Test updating a pet without authentication."""
        data = {"name": "Hacked"}
        response = api_client.patch(f"/v2/pet/{pet.id}/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPetDelete:
    """Tests for deleting pets."""

    def test_delete_pet(self, authenticated_client, pet):
        """Test deleting a pet."""
        pet_id = pet.id
        response = authenticated_client.delete(f"/v2/pet/{pet_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Pet.objects.filter(id=pet_id).exists()

    def test_delete_pet_unauthenticated(self, api_client, pet):
        """Test deleting a pet without authentication."""
        response = api_client.delete(f"/v2/pet/{pet.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPetFindByStatus:
    """Tests for finding pets by status."""

    def test_find_pets_by_single_status(self, api_client, pet):
        """Test finding pets by a single status."""
        response = api_client.get("/v2/pet/findByStatus/?status=available")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        if len(response.data) > 0:
            assert all(p["status"] == "available" for p in response.data)

    def test_find_pets_by_multiple_statuses(self, api_client):
        """Test finding pets by multiple statuses."""
        # Create pets with different statuses
        Pet.objects.create(name="Pet1", status="available")
        Pet.objects.create(name="Pet2", status="pending")

        response = api_client.get("/v2/pet/findByStatus/?status=available,pending")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_find_pets_missing_status_parameter(self, api_client):
        """Test finding pets without status parameter."""
        response = api_client.get("/v2/pet/findByStatus/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_find_pets_invalid_status(self, api_client):
        """Test finding pets with invalid status."""
        response = api_client.get("/v2/pet/findByStatus/?status=invalid")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPetFindByTags:
    """Tests for finding pets by tags."""

    def test_find_pets_by_tags(self, api_client, pet, tag):
        """Test finding pets by tags."""
        response = api_client.get(f"/v2/pet/findByTags/?tags={tag.name}")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_find_pets_missing_tags_parameter(self, api_client):
        """Test finding pets without tags parameter."""
        response = api_client.get("/v2/pet/findByTags/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPetImageUpload:
    """Tests for uploading pet images."""

    def test_upload_image_authenticated(self, authenticated_client, pet):
        """Test uploading image with authentication."""
        from io import BytesIO

        from PIL import Image

        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        response = authenticated_client.post(
            f"/v2/pet/{pet.id}/uploadImage/",
            {"file": img_byte_arr, "additionalMetadata": "Test image"},
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200

    def test_upload_image_without_file(self, authenticated_client, pet):
        """Test uploading image without file."""
        response = authenticated_client.post(
            f"/v2/pet/{pet.id}/uploadImage/",
            {},
            format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCategoryEndpoints:
    """Tests for category endpoints."""

    def test_create_category(self, api_client):
        """Test creating a category."""
        data = {"name": "Cats"}
        response = api_client.post("/v2/pet/categories/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="Cats").exists()

    def test_list_categories(self, api_client, category):
        """Test listing categories."""
        response = api_client.get("/v2/pet/categories/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTagEndpoints:
    """Tests for tag endpoints."""

    def test_create_tag(self, api_client):
        """Test creating a tag."""
        data = {"name": "cute"}
        response = api_client.post("/v2/pet/tags/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Tag.objects.filter(name="cute").exists()

    def test_list_tags(self, api_client, tag):
        """Test listing tags."""
        response = api_client.get("/v2/pet/tags/")

        assert response.status_code == status.HTTP_200_OK
