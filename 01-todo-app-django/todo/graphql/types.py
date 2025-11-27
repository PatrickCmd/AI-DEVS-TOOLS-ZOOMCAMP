"""
GraphQL types for the TODO application.

This module defines Strawberry GraphQL types for the Todo model.
"""

import strawberry
import strawberry_django
from typing import Optional
from datetime import datetime

from todo.models import Todo


@strawberry_django.type(Todo)
class TodoType:
    """
    GraphQL type for Todo model.

    Represents a TODO item with all its fields exposed via GraphQL.
    """
    id: strawberry.ID
    title: str
    description: str
    due_date: Optional[datetime]
    is_resolved: bool
    created_at: datetime
    updated_at: datetime


@strawberry.input
class TodoInput:
    """
    Input type for creating a new TODO.

    Required fields:
    - title: The TODO title

    Optional fields:
    - description: Detailed description
    - due_date: Due date for the TODO
    """
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None


@strawberry.input
class TodoUpdateInput:
    """
    Input type for updating an existing TODO.

    All fields are optional, allowing partial updates.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_resolved: Optional[bool] = None


@strawberry.type
class TodoResponse:
    """
    Response type for TODO mutations.

    Includes success status, optional message, and the TODO item.
    """
    success: bool
    message: Optional[str] = None
    todo: Optional[TodoType] = None


@strawberry.type
class DeleteResponse:
    """
    Response type for delete mutations.

    Indicates success and provides a message.
    """
    success: bool
    message: str


@strawberry.type
class PaginationInfo:
    """
    Pagination information for list queries.
    """
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


@strawberry.type
class TodoConnection:
    """
    Paginated list of TODOs with pagination metadata.
    """
    items: list[TodoType]
    pagination: PaginationInfo
