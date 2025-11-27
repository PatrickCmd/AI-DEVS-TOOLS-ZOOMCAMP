import pytest
from django.urls import reverse
from todo.models import Todo


@pytest.mark.django_db
class TestTemplates:
    def test_base_template_content(self, client):
        """Test that base template contains required elements"""
        response = client.get(reverse("todo_list"))
        content = response.content.decode()
        assert "TODO Application" in content
        assert "Home" in content
        assert "Add TODO" in content

    def test_home_template_with_todos(self, client):
        """Test home template displays TODOs correctly"""
        todo = Todo.objects.create(
            title="Test TODO",
            description="Test description"
        )
        response = client.get(reverse("todo_list"))
        content = response.content.decode()
        assert "Test TODO" in content
        assert "Test description" in content
        assert "Mark Resolved" in content
        assert "Edit" in content
        assert "Delete" in content

    def test_home_template_resolved_todo(self, client):
        """Test that resolved TODOs are displayed differently"""
        todo = Todo.objects.create(
            title="Resolved TODO",
            is_resolved=True
        )
        response = client.get(reverse("todo_list"))
        content = response.content.decode()
        assert "Resolved TODO" in content
        assert "Mark Unresolved" in content

    def test_create_form_template(self, client):
        """Test create form template"""
        response = client.get(reverse("todo_create"))
        content = response.content.decode()
        assert "Create TODO" in content
        assert "Title:" in content
        assert "Description:" in content
        assert "Due Date:" in content
        assert "Save" in content

    def test_edit_form_template(self, client):
        """Test edit form template"""
        todo = Todo.objects.create(title="Test TODO")
        response = client.get(reverse("todo_edit", args=[todo.pk]))
        content = response.content.decode()
        assert "Edit TODO" in content
        assert "Test TODO" in content

    def test_delete_confirmation_template(self, client):
        """Test delete confirmation template"""
        todo = Todo.objects.create(title="Test TODO")
        response = client.get(reverse("todo_delete", args=[todo.pk]))
        content = response.content.decode()
        assert "Delete TODO" in content
        assert "Are you sure" in content
        assert "Test TODO" in content
        assert "Yes, Delete" in content
