import pytest
from django.urls import reverse
from django.utils import timezone
from todo.models import Todo


@pytest.mark.django_db
class TestTodoViews:
    def test_todo_list_view(self, client):
        """Test the TODO list view loads correctly"""
        Todo.objects.create(title="Test TODO 1")
        Todo.objects.create(title="Test TODO 2")

        response = client.get(reverse("todo_list"))
        assert response.status_code == 200
        assert "Test TODO 1" in response.content.decode()
        assert "Test TODO 2" in response.content.decode()

    def test_todo_list_view_empty(self, client):
        """Test the TODO list view with no TODOs"""
        response = client.get(reverse("todo_list"))
        assert response.status_code == 200
        assert "No TODOs yet" in response.content.decode()

    def test_todo_create_view_get(self, client):
        """Test GET request to create TODO view"""
        response = client.get(reverse("todo_create"))
        assert response.status_code == 200
        assert "Create TODO" in response.content.decode()

    def test_todo_create_view_post(self, client):
        """Test creating a TODO via POST request"""
        data = {
            "title": "New TODO",
            "description": "New description",
        }
        response = client.post(reverse("todo_create"), data)
        assert response.status_code == 302
        assert Todo.objects.filter(title="New TODO").exists()

    def test_todo_create_view_post_with_due_date(self, client):
        """Test creating a TODO with due date"""
        due_date = timezone.now() + timezone.timedelta(days=1)
        data = {
            "title": "New TODO",
            "description": "New description",
            "due_date": due_date.strftime("%Y-%m-%dT%H:%M"),
        }
        response = client.post(reverse("todo_create"), data)
        assert response.status_code == 302
        todo = Todo.objects.get(title="New TODO")
        assert todo.due_date is not None

    def test_todo_update_view_get(self, client):
        """Test GET request to update TODO view"""
        todo = Todo.objects.create(title="Test TODO")
        response = client.get(reverse("todo_edit", args=[todo.pk]))
        assert response.status_code == 200
        assert "Edit TODO" in response.content.decode()

    def test_todo_update_view_post(self, client):
        """Test updating a TODO via POST request"""
        todo = Todo.objects.create(title="Original Title")
        data = {
            "title": "Updated Title",
            "description": "Updated description",
        }
        response = client.post(reverse("todo_edit", args=[todo.pk]), data)
        assert response.status_code == 302
        todo.refresh_from_db()
        assert todo.title == "Updated Title"
        assert todo.description == "Updated description"

    def test_todo_delete_view_get(self, client):
        """Test GET request to delete TODO view"""
        todo = Todo.objects.create(title="Test TODO")
        response = client.get(reverse("todo_delete", args=[todo.pk]))
        assert response.status_code == 200
        assert "Delete TODO" in response.content.decode()

    def test_todo_delete_view_post(self, client):
        """Test deleting a TODO via POST request"""
        todo = Todo.objects.create(title="Test TODO")
        response = client.post(reverse("todo_delete", args=[todo.pk]))
        assert response.status_code == 302
        assert not Todo.objects.filter(pk=todo.pk).exists()

    def test_todo_toggle_resolved_view(self, client):
        """Test toggling TODO resolved status"""
        todo = Todo.objects.create(title="Test TODO", is_resolved=False)
        response = client.post(reverse("todo_toggle", args=[todo.pk]))
        assert response.status_code == 302
        todo.refresh_from_db()
        assert todo.is_resolved is True

        response = client.post(reverse("todo_toggle", args=[todo.pk]))
        assert response.status_code == 302
        todo.refresh_from_db()
        assert todo.is_resolved is False

    def test_todo_toggle_resolved_view_not_found(self, client):
        """Test toggling non-existent TODO"""
        response = client.post(reverse("todo_toggle", args=[9999]))
        assert response.status_code == 404
