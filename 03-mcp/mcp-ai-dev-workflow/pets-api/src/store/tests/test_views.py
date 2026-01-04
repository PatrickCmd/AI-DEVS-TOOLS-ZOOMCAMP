"""
Tests for store views and endpoints.
"""

import pytest
from rest_framework import status

from store.models import Order


@pytest.mark.django_db
class TestOrderCreate:
    """Tests for creating orders."""

    def test_create_order_authenticated(self, authenticated_client, pet):
        """Test creating an order with authentication."""
        data = {
            "pet_id": pet.id,
            "quantity": 2,
            "status": "placed"
        }
        response = authenticated_client.post("/v2/store/orders/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["quantity"] == 2
        assert response.data["status"] == "placed"
        assert Order.objects.filter(pet=pet).exists()

    def test_create_order_unauthenticated(self, api_client, pet):
        """Test creating an order without authentication."""
        data = {
            "pet_id": pet.id,
            "quantity": 1,
            "status": "placed"
        }
        response = api_client.post("/v2/store/orders/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_invalid_pet(self, authenticated_client):
        """Test creating an order with nonexistent pet."""
        data = {
            "pet_id": 99999,
            "quantity": 1,
            "status": "placed"
        }
        response = authenticated_client.post("/v2/store/orders/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestOrderList:
    """Tests for listing orders."""

    def test_list_orders_authenticated(self, authenticated_client, order):
        """Test listing orders with authentication."""
        response = authenticated_client.get("/v2/store/orders/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_list_orders_unauthenticated(self, api_client, order):
        """Test listing orders without authentication."""
        response = api_client.get("/v2/store/orders/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderRetrieve:
    """Tests for retrieving a single order."""

    def test_get_order_by_id(self, authenticated_client, order):
        """Test retrieving an order by ID."""
        response = authenticated_client.get(f"/v2/store/orders/{order.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == order.id
        assert response.data["quantity"] == order.quantity

    def test_get_nonexistent_order(self, authenticated_client):
        """Test retrieving a nonexistent order."""
        response = authenticated_client.get("/v2/store/orders/99999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_order_unauthenticated(self, api_client, order):
        """Test retrieving an order without authentication."""
        response = api_client.get(f"/v2/store/orders/{order.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderUpdate:
    """Tests for updating orders."""

    def test_update_order(self, authenticated_client, order):
        """Test updating an order."""
        data = {
            "status": "approved",
            "complete": True
        }
        response = authenticated_client.patch(
            f"/v2/store/orders/{order.id}/",
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "approved"
        assert response.data["complete"] is True

    def test_update_order_unauthenticated(self, api_client, order):
        """Test updating an order without authentication."""
        data = {"status": "approved"}
        response = api_client.patch(
            f"/v2/store/orders/{order.id}/",
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestOrderDelete:
    """Tests for deleting orders."""

    def test_delete_incomplete_order(self, authenticated_client, order):
        """Test deleting an incomplete order (should succeed)."""
        order_id = order.id
        response = authenticated_client.delete(f"/v2/store/orders/{order_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(id=order_id).exists()

    def test_delete_completed_order(self, authenticated_client, order):
        """Test deleting a completed order (should fail)."""
        order.complete = True
        order.save()

        response = authenticated_client.delete(f"/v2/store/orders/{order.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Order.objects.filter(id=order.id).exists()

    def test_delete_order_unauthenticated(self, api_client, order):
        """Test deleting an order without authentication."""
        response = api_client.delete(f"/v2/store/orders/{order.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestInventory:
    """Tests for inventory endpoint."""

    def test_get_inventory(self, api_client):
        """Test getting inventory (public endpoint)."""
        response = api_client.get("/v2/store/orders/inventory/")

        assert response.status_code == status.HTTP_200_OK
        assert "available" in response.data
        assert "pending" in response.data
        assert "sold" in response.data

    def test_inventory_counts(self, api_client, pet):
        """Test inventory counts with actual data."""
        from pets.models import Pet

        # Create pets with different statuses
        Pet.objects.create(name="Available Pet", status="available")
        Pet.objects.create(name="Pending Pet", status="pending")
        Pet.objects.create(name="Sold Pet", status="sold")

        response = api_client.get("/v2/store/orders/inventory/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["available"] >= 1
        assert response.data["pending"] >= 1
        assert response.data["sold"] >= 1
