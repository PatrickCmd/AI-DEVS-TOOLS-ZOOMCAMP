"""
API views for the TODO application.

This module contains ViewSets for the REST API using Django REST Framework.
Provides CRUD operations and custom actions for managing TODO items.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from django.utils import timezone

from todo.models import Todo
from .serializers import TodoSerializer, TodoListSerializer, TodoToggleSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all TODOs",
        description="Retrieve a paginated list of all TODO items. Supports filtering, searching, and ordering.",
        parameters=[
            OpenApiParameter(
                name='is_resolved',
                description='Filter by resolved status (true/false)',
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name='search',
                description='Search in title and description',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='ordering',
                description='Order results by field (prefix with - for descending). Options: created_at, due_date, title',
                required=False,
                type=str
            ),
        ],
        responses={200: TodoListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Retrieve a TODO",
        description="Get detailed information about a specific TODO item by ID.",
        responses={
            200: TodoSerializer,
            404: OpenApiResponse(description="TODO not found")
        }
    ),
    create=extend_schema(
        summary="Create a new TODO",
        description="Create a new TODO item with title, description, and optional due date.",
        request=TodoSerializer,
        responses={
            201: TodoSerializer,
            400: OpenApiResponse(description="Validation error")
        }
    ),
    update=extend_schema(
        summary="Update a TODO",
        description="Update all fields of an existing TODO item.",
        request=TodoSerializer,
        responses={
            200: TodoSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="TODO not found")
        }
    ),
    partial_update=extend_schema(
        summary="Partially update a TODO",
        description="Update one or more fields of an existing TODO item.",
        request=TodoSerializer,
        responses={
            200: TodoSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="TODO not found")
        }
    ),
    destroy=extend_schema(
        summary="Delete a TODO",
        description="Permanently delete a TODO item.",
        responses={
            204: OpenApiResponse(description="TODO deleted successfully"),
            404: OpenApiResponse(description="TODO not found")
        }
    ),
)
class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TODO CRUD operations.

    Provides:
    - list: GET /api/todos/
    - retrieve: GET /api/todos/{id}/
    - create: POST /api/todos/
    - update: PUT /api/todos/{id}/
    - partial_update: PATCH /api/todos/{id}/
    - destroy: DELETE /api/todos/{id}/
    - toggle_resolved: POST /api/todos/{id}/toggle_resolved/
    - resolved: GET /api/todos/resolved/
    - unresolved: GET /api/todos/unresolved/
    - overdue: GET /api/todos/overdue/
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'title', 'is_resolved']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use TodoListSerializer for list view for better performance.
        Use TodoToggleSerializer for toggle_resolved action.
        """
        if self.action == 'list':
            return TodoListSerializer
        elif self.action == 'toggle_resolved':
            return TodoToggleSerializer
        return TodoSerializer

    def get_queryset(self):
        """
        Optionally filter queryset by is_resolved status.
        """
        queryset = Todo.objects.all()

        # Filter by is_resolved status if provided
        is_resolved = self.request.query_params.get('is_resolved', None)
        if is_resolved is not None:
            is_resolved_bool = is_resolved.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(is_resolved=is_resolved_bool)

        return queryset

    @extend_schema(
        summary="Toggle TODO resolved status",
        description="Toggle the is_resolved status of a TODO item between true and false.",
        request=None,
        responses={
            200: TodoSerializer,
            404: OpenApiResponse(description="TODO not found")
        }
    )
    @action(detail=True, methods=['post'])
    def toggle_resolved(self, request, pk=None):
        """
        Custom action to toggle the is_resolved status of a TODO.
        """
        todo = self.get_object()
        todo.is_resolved = not todo.is_resolved
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    @extend_schema(
        summary="List resolved TODOs",
        description="Retrieve a paginated list of all resolved TODO items.",
        responses={200: TodoListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def resolved(self, request):
        """
        Custom action to list only resolved TODOs.
        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_resolved=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TodoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TodoListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="List unresolved TODOs",
        description="Retrieve a paginated list of all unresolved TODO items.",
        responses={200: TodoListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        """
        Custom action to list only unresolved TODOs.
        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_resolved=False))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TodoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TodoListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="List overdue TODOs",
        description="Retrieve a paginated list of all unresolved TODO items with due dates in the past.",
        responses={200: TodoListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """
        Custom action to list overdue TODOs (unresolved with due_date in the past).
        """
        now = timezone.now()
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                is_resolved=False,
                due_date__lt=now
            )
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TodoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TodoListSerializer(queryset, many=True)
        return Response(serializer.data)
