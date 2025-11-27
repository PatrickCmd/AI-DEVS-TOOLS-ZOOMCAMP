import pytest
from django.urls import reverse, resolve
from todo.views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    TodoToggleResolvedView,
)


class TestUrls:
    def test_todo_list_url_resolves(self):
        """Test that todo_list URL resolves to correct view"""
        url = reverse("todo_list")
        assert resolve(url).func.view_class == TodoListView

    def test_todo_create_url_resolves(self):
        """Test that todo_create URL resolves to correct view"""
        url = reverse("todo_create")
        assert resolve(url).func.view_class == TodoCreateView

    def test_todo_edit_url_resolves(self):
        """Test that todo_edit URL resolves to correct view"""
        url = reverse("todo_edit", args=[1])
        assert resolve(url).func.view_class == TodoUpdateView

    def test_todo_delete_url_resolves(self):
        """Test that todo_delete URL resolves to correct view"""
        url = reverse("todo_delete", args=[1])
        assert resolve(url).func.view_class == TodoDeleteView

    def test_todo_toggle_url_resolves(self):
        """Test that todo_toggle URL resolves to correct view"""
        url = reverse("todo_toggle", args=[1])
        assert resolve(url).func.view_class == TodoToggleResolvedView
