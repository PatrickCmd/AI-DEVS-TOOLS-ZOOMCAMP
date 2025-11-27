"""
Tests for the TODO REST API.

This module contains comprehensive tests for all API endpoints including
CRUD operations, custom actions, filtering, searching, and pagination.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from todo.models import Todo


@pytest.fixture
def api_client():
    """Fixture for DRF API client."""
    return APIClient()


@pytest.fixture
def sample_todo():
    """Fixture for creating a sample TODO."""
    return Todo.objects.create(
        title="Test TODO",
        description="Test description",
        due_date=timezone.now() + timedelta(days=1)
    )


@pytest.fixture
def multiple_todos():
    """Fixture for creating multiple TODOs."""
    todos = []
    for i in range(5):
        todo = Todo.objects.create(
            title=f"TODO {i}",
            description=f"Description {i}",
            is_resolved=(i % 2 == 0)
        )
        todos.append(todo)
    return todos


@pytest.fixture
def overdue_todo():
    """Fixture for creating an overdue TODO."""
    return Todo.objects.create(
        title="Overdue TODO",
        description="This is overdue",
        due_date=timezone.now() - timedelta(days=1),
        is_resolved=False
    )


@pytest.mark.django_db
class TestTodoListAPI:
    """Tests for listing TODOs via API."""

    def test_list_todos_empty(self, api_client):
        """Test listing TODOs when none exist."""
        url = reverse('todo-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        assert response.data['results'] == []

    def test_list_todos(self, api_client, multiple_todos):
        """Test listing all TODOs."""
        url = reverse('todo-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 5
        assert len(response.data['results']) == 5

    def test_list_todos_pagination(self, api_client):
        """Test pagination of TODO list."""
        # Create more TODOs than the page size (10)
        for i in range(15):
            Todo.objects.create(title=f"TODO {i}", description=f"Description {i}")

        url = reverse('todo-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 15
        assert len(response.data['results']) == 10  # PAGE_SIZE is 10
        assert response.data['next'] is not None

    def test_list_todos_filter_resolved(self, api_client, multiple_todos):
        """Test filtering TODOs by resolved status."""
        url = reverse('todo-list')
        response = api_client.get(url, {'is_resolved': 'true'})

        assert response.status_code == status.HTTP_200_OK
        # 3 out of 5 are resolved (0, 2, 4)
        assert response.data['count'] == 3

        response = api_client.get(url, {'is_resolved': 'false'})
        assert response.data['count'] == 2

    def test_list_todos_search(self, api_client):
        """Test searching TODOs by title or description."""
        Todo.objects.create(title="Buy groceries", description="Milk and eggs")
        Todo.objects.create(title="Doctor appointment", description="Check-up")

        url = reverse('todo-list')
        response = api_client.get(url, {'search': 'groceries'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert 'groceries' in response.data['results'][0]['title'].lower()

    def test_list_todos_ordering(self, api_client, multiple_todos):
        """Test ordering TODOs."""
        url = reverse('todo-list')

        # Default ordering is -created_at
        response = api_client.get(url)
        titles = [todo['title'] for todo in response.data['results']]
        assert titles == ['TODO 4', 'TODO 3', 'TODO 2', 'TODO 1', 'TODO 0']

        # Order by title ascending
        response = api_client.get(url, {'ordering': 'title'})
        titles = [todo['title'] for todo in response.data['results']]
        assert titles == ['TODO 0', 'TODO 1', 'TODO 2', 'TODO 3', 'TODO 4']


@pytest.mark.django_db
class TestTodoRetrieveAPI:
    """Tests for retrieving a single TODO via API."""

    def test_retrieve_todo(self, api_client, sample_todo):
        """Test retrieving a specific TODO."""
        url = reverse('todo-detail', kwargs={'pk': sample_todo.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_todo.pk
        assert response.data['title'] == sample_todo.title
        assert response.data['description'] == sample_todo.description
        assert 'created_at' in response.data
        assert 'updated_at' in response.data

    def test_retrieve_nonexistent_todo(self, api_client):
        """Test retrieving a TODO that doesn't exist."""
        url = reverse('todo-detail', kwargs={'pk': 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTodoCreateAPI:
    """Tests for creating TODOs via API."""

    def test_create_todo_minimal(self, api_client):
        """Test creating a TODO with only required fields."""
        url = reverse('todo-list')
        data = {
            'title': 'New TODO',
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New TODO'
        assert response.data['description'] == ''
        assert response.data['is_resolved'] is False
        assert Todo.objects.count() == 1

    def test_create_todo_full(self, api_client):
        """Test creating a TODO with all fields."""
        url = reverse('todo-list')
        due_date = timezone.now() + timedelta(days=7)
        data = {
            'title': 'Complete TODO',
            'description': 'Full description',
            'due_date': due_date.isoformat(),
            'is_resolved': False
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Complete TODO'
        assert response.data['description'] == 'Full description'
        assert response.data['is_resolved'] is False

    def test_create_todo_empty_title(self, api_client):
        """Test creating a TODO with empty title fails."""
        url = reverse('todo-list')
        data = {
            'title': '',
            'description': 'No title'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data

    def test_create_todo_whitespace_title(self, api_client):
        """Test creating a TODO with whitespace-only title fails."""
        url = reverse('todo-list')
        data = {
            'title': '   ',
            'description': 'Whitespace title'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_todo_missing_title(self, api_client):
        """Test creating a TODO without title fails."""
        url = reverse('todo-list')
        data = {
            'description': 'Missing title'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data

    def test_create_todo_past_due_date(self, api_client):
        """Test creating a TODO with past due date fails."""
        url = reverse('todo-list')
        past_date = timezone.now() - timedelta(days=1)
        data = {
            'title': 'Past TODO',
            'due_date': past_date.isoformat()
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'due_date' in response.data


@pytest.mark.django_db
class TestTodoUpdateAPI:
    """Tests for updating TODOs via API."""

    def test_update_todo_full(self, api_client, sample_todo):
        """Test full update (PUT) of a TODO."""
        url = reverse('todo-detail', kwargs={'pk': sample_todo.pk})
        new_due_date = timezone.now() + timedelta(days=3)
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'due_date': new_due_date.isoformat(),
            'is_resolved': True
        }
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['description'] == 'Updated description'
        assert response.data['is_resolved'] is True

        sample_todo.refresh_from_db()
        assert sample_todo.title == 'Updated Title'
        assert sample_todo.is_resolved is True

    def test_partial_update_todo(self, api_client, sample_todo):
        """Test partial update (PATCH) of a TODO."""
        url = reverse('todo-detail', kwargs={'pk': sample_todo.pk})
        data = {
            'title': 'Partially Updated'
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Partially Updated'
        assert response.data['description'] == sample_todo.description

    def test_update_nonexistent_todo(self, api_client):
        """Test updating a TODO that doesn't exist."""
        url = reverse('todo-detail', kwargs={'pk': 9999})
        data = {'title': 'Updated'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTodoDeleteAPI:
    """Tests for deleting TODOs via API."""

    def test_delete_todo(self, api_client, sample_todo):
        """Test deleting a TODO."""
        url = reverse('todo-detail', kwargs={'pk': sample_todo.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Todo.objects.count() == 0

    def test_delete_nonexistent_todo(self, api_client):
        """Test deleting a TODO that doesn't exist."""
        url = reverse('todo-detail', kwargs={'pk': 9999})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestTodoToggleResolvedAPI:
    """Tests for toggling TODO resolved status via API."""

    def test_toggle_resolved_to_true(self, api_client, sample_todo):
        """Test toggling unresolved TODO to resolved."""
        assert sample_todo.is_resolved is False

        url = reverse('todo-toggle-resolved', kwargs={'pk': sample_todo.pk})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_resolved'] is True

        sample_todo.refresh_from_db()
        assert sample_todo.is_resolved is True

    def test_toggle_resolved_to_false(self, api_client, sample_todo):
        """Test toggling resolved TODO to unresolved."""
        sample_todo.is_resolved = True
        sample_todo.save()

        url = reverse('todo-toggle-resolved', kwargs={'pk': sample_todo.pk})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_resolved'] is False

        sample_todo.refresh_from_db()
        assert sample_todo.is_resolved is False

    def test_toggle_resolved_multiple_times(self, api_client, sample_todo):
        """Test toggling resolved status multiple times."""
        url = reverse('todo-toggle-resolved', kwargs={'pk': sample_todo.pk})

        # Toggle 1
        response = api_client.post(url)
        assert response.data['is_resolved'] is True

        # Toggle 2
        response = api_client.post(url)
        assert response.data['is_resolved'] is False

        # Toggle 3
        response = api_client.post(url)
        assert response.data['is_resolved'] is True


@pytest.mark.django_db
class TestTodoCustomActionsAPI:
    """Tests for custom API actions."""

    def test_resolved_action(self, api_client, multiple_todos):
        """Test /api/todos/resolved/ endpoint."""
        url = reverse('todo-resolved')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # 3 out of 5 are resolved
        assert response.data['count'] == 3

        for todo in response.data['results']:
            # Note: is_resolved field is not in TodoListSerializer
            # but we can verify by checking which todos are returned
            pass

    def test_unresolved_action(self, api_client, multiple_todos):
        """Test /api/todos/unresolved/ endpoint."""
        url = reverse('todo-unresolved')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # 2 out of 5 are unresolved
        assert response.data['count'] == 2

    def test_overdue_action(self, api_client, overdue_todo):
        """Test /api/todos/overdue/ endpoint."""
        # Create a non-overdue TODO
        Todo.objects.create(
            title="Not overdue",
            due_date=timezone.now() + timedelta(days=1),
            is_resolved=False
        )

        # Create a resolved overdue TODO (should not appear)
        Todo.objects.create(
            title="Resolved overdue",
            due_date=timezone.now() - timedelta(days=1),
            is_resolved=True
        )

        url = reverse('todo-overdue')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Only the unresolved overdue TODO
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == "Overdue TODO"

    def test_overdue_action_empty(self, api_client, sample_todo):
        """Test overdue endpoint when no TODOs are overdue."""
        url = reverse('todo-overdue')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0


@pytest.mark.django_db
class TestAPIContentTypes:
    """Tests for API content types and formats."""

    def test_json_content_type(self, api_client, sample_todo):
        """Test that API returns JSON content type."""
        url = reverse('todo-detail', kwargs={'pk': sample_todo.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response['Content-Type']

    def test_create_with_json(self, api_client):
        """Test creating a TODO with JSON content type."""
        url = reverse('todo-list')
        data = {
            'title': 'JSON TODO',
            'description': 'Created with JSON'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'JSON TODO'


@pytest.mark.django_db
class TestAPISchema:
    """Tests for API schema and documentation endpoints."""

    def test_schema_endpoint(self, api_client):
        """Test that API schema endpoint is accessible."""
        url = reverse('schema')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Schema should be YAML format by default
        assert 'openapi' in response.data or b'openapi' in response.content

    def test_swagger_ui_endpoint(self, api_client):
        """Test that Swagger UI endpoint is accessible."""
        url = reverse('swagger-ui')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_redoc_endpoint(self, api_client):
        """Test that ReDoc endpoint is accessible."""
        url = reverse('redoc')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
