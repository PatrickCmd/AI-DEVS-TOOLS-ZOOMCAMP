import pytest
from django.utils import timezone
from todo.models import Todo


@pytest.mark.django_db
class TestTodoModel:
    def test_create_todo(self):
        """Test creating a new TODO"""
        todo = Todo.objects.create(
            title="Test TODO",
            description="Test description"
        )
        assert todo.title == "Test TODO"
        assert todo.description == "Test description"
        assert todo.is_resolved is False
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_create_todo_with_due_date(self):
        """Test creating a TODO with a due date"""
        due_date = timezone.now() + timezone.timedelta(days=1)
        todo = Todo.objects.create(
            title="Test TODO",
            due_date=due_date
        )
        assert todo.due_date == due_date

    def test_todo_str_representation(self):
        """Test TODO string representation"""
        todo = Todo.objects.create(title="Test TODO")
        assert str(todo) == "Test TODO"

    def test_todo_ordering(self):
        """Test that TODOs are ordered by created_at descending"""
        todo1 = Todo.objects.create(title="First TODO")
        todo2 = Todo.objects.create(title="Second TODO")
        todos = list(Todo.objects.all())
        assert todos[0].title == "Second TODO"
        assert todos[1].title == "First TODO"

    def test_mark_todo_resolved(self):
        """Test marking a TODO as resolved"""
        todo = Todo.objects.create(title="Test TODO")
        assert todo.is_resolved is False
        todo.is_resolved = True
        todo.save()
        todo.refresh_from_db()
        assert todo.is_resolved is True

    def test_edit_todo(self):
        """Test editing a TODO"""
        todo = Todo.objects.create(
            title="Original Title",
            description="Original Description"
        )
        todo.title = "Updated Title"
        todo.description = "Updated Description"
        todo.save()
        todo.refresh_from_db()
        assert todo.title == "Updated Title"
        assert todo.description == "Updated Description"

    def test_delete_todo(self):
        """Test deleting a TODO"""
        todo = Todo.objects.create(title="Test TODO")
        todo_id = todo.id
        todo.delete()
        assert not Todo.objects.filter(id=todo_id).exists()
