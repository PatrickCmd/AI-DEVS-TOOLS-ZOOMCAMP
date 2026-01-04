"""
Tests for store models.
"""

from datetime import UTC

import pytest
from django.contrib.auth import get_user_model

from store.models import Order

User = get_user_model()


@pytest.mark.django_db
class TestOrderModel:
    """Tests for the Order model."""

    def test_create_order(self, pet, user):
        """Test creating an order."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=2,
            status="placed"
        )

        assert order.pet == pet
        assert order.user == user
        assert order.quantity == 2
        assert order.status == "placed"
        assert not order.complete

    def test_order_str_representation(self, pet, user):
        """Test order string representation."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1,
            status="placed"
        )

        expected = f"Order #{order.id} - {pet.name} (Placed)"
        assert str(order) == expected

    def test_order_repr(self, pet, user):
        """Test order representation."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1,
            status="placed"
        )

        assert repr(order) == f"<Order id={order.id}, pet={pet.id}, status=placed>"

    def test_order_default_status(self, pet, user):
        """Test order default status is 'placed'."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1
        )

        assert order.status == "placed"

    def test_order_default_quantity(self, pet, user):
        """Test order default quantity is 1."""
        order = Order.objects.create(
            pet=pet,
            user=user
        )

        assert order.quantity == 1

    def test_order_without_user(self, pet):
        """Test creating order without user (guest order)."""
        order = Order.objects.create(
            pet=pet,
            quantity=1,
            status="placed"
        )

        assert order.user is None
        assert order.pet == pet

    def test_order_status_choices(self):
        """Test order status choices."""
        assert Order.Status.PLACED == "placed"
        assert Order.Status.APPROVED == "approved"
        assert Order.Status.DELIVERED == "delivered"

    def test_order_complete_field(self, pet, user):
        """Test order complete field."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1,
            status="delivered",
            complete=True
        )

        assert order.complete is True

    def test_order_ordering(self, pet, user):
        """Test that orders are ordered by created_at descending."""
        order1 = Order.objects.create(pet=pet, user=user, quantity=1)
        order2 = Order.objects.create(pet=pet, user=user, quantity=2)

        orders = Order.objects.all()
        assert orders[0] == order2  # Most recent first
        assert orders[1] == order1

    def test_order_with_ship_date(self, pet, user):
        """Test order with ship date."""
        from datetime import datetime

        ship_date = datetime.now(UTC)
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1,
            ship_date=ship_date
        )

        assert order.ship_date is not None
        assert order.ship_date == ship_date

    def test_order_pet_deletion_cascade(self, pet, user):
        """Test that deleting pet cascades to orders."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1
        )
        order_id = order.id

        pet.delete()

        assert not Order.objects.filter(id=order_id).exists()

    def test_order_user_deletion_cascade(self, pet, user):
        """Test that deleting user cascades to orders."""
        order = Order.objects.create(
            pet=pet,
            user=user,
            quantity=1
        )
        order_id = order.id

        user.delete()

        assert not Order.objects.filter(id=order_id).exists()
