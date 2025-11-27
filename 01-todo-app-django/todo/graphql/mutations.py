"""
GraphQL mutations for the TODO application.

This module defines all GraphQL mutations for creating, updating, and deleting TODO items.
"""

import strawberry
from django.utils import timezone

from todo.models import Todo
from .types import TodoInput, TodoUpdateInput, TodoResponse, DeleteResponse, TodoType


@strawberry.type
class Mutation:
    """
    Root Mutation type for GraphQL API.

    Provides mutations for creating, updating, and deleting TODO items.
    """

    @strawberry.mutation
    def create_todo(self, input: TodoInput) -> TodoResponse:
        """
        Create a new TODO item.

        Args:
            input: TodoInput with title, description, and due_date

        Returns:
            TodoResponse with success status and created TODO
        """
        # Validate title
        if not input.title or not input.title.strip():
            return TodoResponse(
                success=False,
                message="Title cannot be empty or whitespace only.",
                todo=None
            )

        # Validate due_date is not in the past
        if input.due_date and input.due_date < timezone.now():
            return TodoResponse(
                success=False,
                message="Due date cannot be in the past.",
                todo=None
            )

        # Create TODO
        try:
            todo = Todo.objects.create(
                title=input.title.strip(),
                description=input.description or "",
                due_date=input.due_date
            )
            return TodoResponse(
                success=True,
                message="TODO created successfully.",
                todo=todo
            )
        except Exception as e:
            return TodoResponse(
                success=False,
                message=f"Failed to create TODO: {str(e)}",
                todo=None
            )

    @strawberry.mutation
    def update_todo(self, id: strawberry.ID, input: TodoUpdateInput) -> TodoResponse:
        """
        Update an existing TODO item.

        Args:
            id: TODO ID
            input: TodoUpdateInput with fields to update

        Returns:
            TodoResponse with success status and updated TODO
        """
        try:
            todo = Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            return TodoResponse(
                success=False,
                message=f"TODO with ID {id} not found.",
                todo=None
            )

        # Update fields if provided
        if input.title is not None:
            if not input.title or not input.title.strip():
                return TodoResponse(
                    success=False,
                    message="Title cannot be empty or whitespace only.",
                    todo=None
                )
            todo.title = input.title.strip()

        if input.description is not None:
            todo.description = input.description

        if input.due_date is not None:
            todo.due_date = input.due_date

        if input.is_resolved is not None:
            todo.is_resolved = input.is_resolved

        try:
            todo.save()
            return TodoResponse(
                success=True,
                message="TODO updated successfully.",
                todo=todo
            )
        except Exception as e:
            return TodoResponse(
                success=False,
                message=f"Failed to update TODO: {str(e)}",
                todo=None
            )

    @strawberry.mutation
    def delete_todo(self, id: strawberry.ID) -> DeleteResponse:
        """
        Delete a TODO item.

        Args:
            id: TODO ID

        Returns:
            DeleteResponse with success status and message
        """
        try:
            todo = Todo.objects.get(pk=id)
            title = todo.title
            todo.delete()
            return DeleteResponse(
                success=True,
                message=f"TODO '{title}' deleted successfully."
            )
        except Todo.DoesNotExist:
            return DeleteResponse(
                success=False,
                message=f"TODO with ID {id} not found."
            )
        except Exception as e:
            return DeleteResponse(
                success=False,
                message=f"Failed to delete TODO: {str(e)}"
            )

    @strawberry.mutation
    def toggle_resolved(self, id: strawberry.ID) -> TodoResponse:
        """
        Toggle the resolved status of a TODO item.

        Args:
            id: TODO ID

        Returns:
            TodoResponse with success status and updated TODO
        """
        try:
            todo = Todo.objects.get(pk=id)
            todo.is_resolved = not todo.is_resolved
            todo.save()
            status = "resolved" if todo.is_resolved else "unresolved"
            return TodoResponse(
                success=True,
                message=f"TODO marked as {status}.",
                todo=todo
            )
        except Todo.DoesNotExist:
            return TodoResponse(
                success=False,
                message=f"TODO with ID {id} not found.",
                todo=None
            )
        except Exception as e:
            return TodoResponse(
                success=False,
                message=f"Failed to toggle TODO status: {str(e)}",
                todo=None
            )

    @strawberry.mutation
    def mark_resolved(self, id: strawberry.ID) -> TodoResponse:
        """
        Mark a TODO as resolved.

        Args:
            id: TODO ID

        Returns:
            TodoResponse with success status and updated TODO
        """
        try:
            todo = Todo.objects.get(pk=id)
            todo.is_resolved = True
            todo.save()
            return TodoResponse(
                success=True,
                message="TODO marked as resolved.",
                todo=todo
            )
        except Todo.DoesNotExist:
            return TodoResponse(
                success=False,
                message=f"TODO with ID {id} not found.",
                todo=None
            )

    @strawberry.mutation
    def mark_unresolved(self, id: strawberry.ID) -> TodoResponse:
        """
        Mark a TODO as unresolved.

        Args:
            id: TODO ID

        Returns:
            TodoResponse with success status and updated TODO
        """
        try:
            todo = Todo.objects.get(pk=id)
            todo.is_resolved = False
            todo.save()
            return TodoResponse(
                success=True,
                message="TODO marked as unresolved.",
                todo=todo
            )
        except Todo.DoesNotExist:
            return TodoResponse(
                success=False,
                message=f"TODO with ID {id} not found.",
                todo=None
            )
