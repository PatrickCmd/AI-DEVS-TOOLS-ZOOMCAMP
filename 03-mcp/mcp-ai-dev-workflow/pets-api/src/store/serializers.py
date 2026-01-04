"""
Store serializers for the Petstore API.
"""

from rest_framework import serializers

from pets.serializers import PetSerializer
from store.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model with nested pet details.
    """

    pet = PetSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "pet",
            "user",
            "quantity",
            "ship_date",
            "status",
            "complete",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user"]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new order.
    """

    pet_id = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = [
            "pet_id",
            "quantity",
            "ship_date",
            "status",
            "complete",
        ]

    def validate_pet_id(self, value):
        """Validate that the pet exists."""
        from pets.models import Pet

        if not Pet.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Pet with id {value} does not exist.")
        return value

    def create(self, validated_data):
        """Create a new order."""
        pet_id = validated_data.pop('pet_id')
        user = self.context['request'].user if 'request' in self.context else None

        order = Order.objects.create(
            pet_id=pet_id,
            user=user if user and user.is_authenticated else None,
            **validated_data
        )
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing order.
    """

    class Meta:
        model = Order
        fields = [
            "quantity",
            "ship_date",
            "status",
            "complete",
        ]

    def update(self, instance, validated_data):
        """Update order instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class InventorySerializer(serializers.Serializer):
    """
    Serializer for inventory status response.
    """

    available = serializers.IntegerField(read_only=True)
    pending = serializers.IntegerField(read_only=True)
    sold = serializers.IntegerField(read_only=True)
