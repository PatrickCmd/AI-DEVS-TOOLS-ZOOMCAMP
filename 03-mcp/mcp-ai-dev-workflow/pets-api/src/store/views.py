"""
Store views for the Petstore API.
"""

from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from pets.models import Pet
from store.models import Order
from store.serializers import (
    InventorySerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order model.
    Provides CRUD operations and custom actions for orders.
    """

    queryset = Order.objects.select_related("pet", "user").all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "complete", "user"]
    ordering_fields = ["created_at", "status", "ship_date"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return OrderUpdateSerializer
        return OrderSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == "inventory":
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create a new order."""
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Return the created order with full details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing order."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Return the updated order with full details
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data)

    @action(detail=False, methods=["get"], url_path="inventory")
    def inventory(self, request):
        """
        Get inventory status.
        Returns counts of pets by their status.
        """
        # Count pets by status
        pet_counts = Pet.objects.values("status").annotate(count=Count("id"))

        # Create a dictionary with all statuses initialized to 0
        inventory = {
            "available": 0,
            "pending": 0,
            "sold": 0,
        }

        # Update with actual counts
        for item in pet_counts:
            status_key = item["status"]
            if status_key in inventory:
                inventory[status_key] = item["count"]

        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete an order."""
        instance = self.get_object()

        # Only allow deletion if order is not completed
        if instance.complete:
            return Response(
                {"error": "Cannot delete a completed order"},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
