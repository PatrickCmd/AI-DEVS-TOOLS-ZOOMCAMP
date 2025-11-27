"""
GraphQL queries for the TODO application.

This module defines all GraphQL queries for retrieving TODO items.
"""

import strawberry
from typing import Optional, List
from django.utils import timezone
from django.db.models import Q

from todo.models import Todo
from .types import TodoType, TodoConnection, PaginationInfo


@strawberry.type
class Query:
    """
    Root Query type for GraphQL API.

    Provides queries for retrieving TODO items with various filters.
    """

    @strawberry.field
    def todos(
        self,
        page: int = 1,
        page_size: int = 10,
        is_resolved: Optional[bool] = None,
        search: Optional[str] = None,
        order_by: Optional[str] = "-created_at"
    ) -> TodoConnection:
        """
        Retrieve a paginated list of TODOs.

        Args:
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10)
            is_resolved: Filter by resolved status (optional)
            search: Search in title and description (optional)
            order_by: Field to order by (default: -created_at)

        Returns:
            TodoConnection with items and pagination info
        """
        queryset = Todo.objects.all()

        # Apply filters
        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)

        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size

        items = list(queryset[start:end])

        pagination = PaginationInfo(
            total=total,
            page=page,
            page_size=page_size,
            has_next=end < total,
            has_previous=page > 1
        )

        return TodoConnection(items=items, pagination=pagination)

    @strawberry.field
    def todo(self, id: strawberry.ID) -> Optional[TodoType]:
        """
        Retrieve a single TODO by ID.

        Args:
            id: TODO ID

        Returns:
            TodoType or None if not found
        """
        try:
            return Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            return None

    @strawberry.field
    def resolved_todos(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> TodoConnection:
        """
        Retrieve a paginated list of resolved TODOs.

        Args:
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10)

        Returns:
            TodoConnection with resolved items
        """
        queryset = Todo.objects.filter(is_resolved=True).order_by('-created_at')

        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size

        items = list(queryset[start:end])

        pagination = PaginationInfo(
            total=total,
            page=page,
            page_size=page_size,
            has_next=end < total,
            has_previous=page > 1
        )

        return TodoConnection(items=items, pagination=pagination)

    @strawberry.field
    def unresolved_todos(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> TodoConnection:
        """
        Retrieve a paginated list of unresolved TODOs.

        Args:
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10)

        Returns:
            TodoConnection with unresolved items
        """
        queryset = Todo.objects.filter(is_resolved=False).order_by('-created_at')

        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size

        items = list(queryset[start:end])

        pagination = PaginationInfo(
            total=total,
            page=page,
            page_size=page_size,
            has_next=end < total,
            has_previous=page > 1
        )

        return TodoConnection(items=items, pagination=pagination)

    @strawberry.field
    def overdue_todos(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> TodoConnection:
        """
        Retrieve a paginated list of overdue TODOs.

        Overdue TODOs are unresolved items with due_date in the past.

        Args:
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10)

        Returns:
            TodoConnection with overdue items
        """
        queryset = Todo.objects.filter(
            is_resolved=False,
            due_date__lt=timezone.now()
        ).order_by('-created_at')

        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size

        items = list(queryset[start:end])

        pagination = PaginationInfo(
            total=total,
            page=page,
            page_size=page_size,
            has_next=end < total,
            has_previous=page > 1
        )

        return TodoConnection(items=items, pagination=pagination)

    @strawberry.field
    def search_todos(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10
    ) -> TodoConnection:
        """
        Search TODOs by title or description.

        Args:
            query: Search query string
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10)

        Returns:
            TodoConnection with matching items
        """
        queryset = Todo.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')

        # Calculate pagination
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size

        items = list(queryset[start:end])

        pagination = PaginationInfo(
            total=total,
            page=page,
            page_size=page_size,
            has_next=end < total,
            has_previous=page > 1
        )

        return TodoConnection(items=items, pagination=pagination)
