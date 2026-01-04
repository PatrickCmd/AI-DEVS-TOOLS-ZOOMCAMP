"""
Pet serializers for the Petstore API.
"""

from rest_framework import serializers

from pets.models import Category, Pet, Tag


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer for Pet model with nested relationships.
    """

    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "category",
            "photo_urls",
            "tags",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PetCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new pet.
    """

    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        default=list
    )

    class Meta:
        model = Pet
        fields = [
            "name",
            "category_id",
            "photo_urls",
            "tag_ids",
            "status",
        ]

    def validate_category_id(self, value):
        """Validate that category exists."""
        if value is not None and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Category with id {value} does not exist.")
        return value

    def validate_tag_ids(self, value):
        """Validate that all tags exist."""
        if value:
            existing_tags = set(Tag.objects.filter(id__in=value).values_list('id', flat=True))
            missing_tags = set(value) - existing_tags
            if missing_tags:
                raise serializers.ValidationError(f"Tags with ids {missing_tags} do not exist.")
        return value

    def create(self, validated_data):
        """Create a new pet with category and tags."""
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])

        pet = Pet.objects.create(
            category_id=category_id,
            **validated_data
        )

        if tag_ids:
            pet.tags.set(tag_ids)

        return pet


class PetUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing pet.
    """

    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Pet
        fields = [
            "name",
            "category_id",
            "photo_urls",
            "tag_ids",
            "status",
        ]

    def validate_category_id(self, value):
        """Validate that category exists."""
        if value is not None and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Category with id {value} does not exist.")
        return value

    def validate_tag_ids(self, value):
        """Validate that all tags exist."""
        if value:
            existing_tags = set(Tag.objects.filter(id__in=value).values_list('id', flat=True))
            missing_tags = set(value) - existing_tags
            if missing_tags:
                raise serializers.ValidationError(f"Tags with ids {missing_tags} do not exist.")
        return value

    def update(self, instance, validated_data):
        """Update pet instance with category and tags."""
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'category_id' in self.initial_data:
            instance.category_id = category_id

        if tag_ids is not None:
            instance.tags.set(tag_ids)

        instance.save()
        return instance
