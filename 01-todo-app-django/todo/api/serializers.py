"""
Serializers for the TODO API.

This module contains serializers for converting TODO model instances
to/from JSON for the REST API.
"""

from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Todo model.

    Provides full CRUD serialization with validation for TODO items.
    Read-only fields (id, created_at, updated_at) are automatically managed.
    """

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'is_resolved',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate that title is not empty or whitespace only.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty or whitespace only.")
        return value.strip()

    def validate_due_date(self, value):
        """
        Validate that due_date is not in the past for new TODOs.
        """
        from django.utils import timezone

        if value and value < timezone.now():
            # Allow past dates for updates, but warn for new TODOs
            if not self.instance:
                raise serializers.ValidationError("Due date cannot be in the past.")

        return value


class TodoListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for TODO list views.

    Excludes description field for better performance on list endpoints.
    Useful when fetching multiple TODOs where full details aren't needed.
    """

    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'due_date',
            'is_resolved',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class TodoToggleSerializer(serializers.ModelSerializer):
    """
    Serializer for toggling the is_resolved status.

    Only allows updating the is_resolved field, preventing
    accidental modification of other TODO properties.
    """

    class Meta:
        model = Todo
        fields = ['id', 'is_resolved']
        read_only_fields = ['id']
