from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    TodoToggleResolvedView,
)

urlpatterns = [
    path("", TodoListView.as_view(), name="todo_list"),
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("<int:pk>/edit/", TodoUpdateView.as_view(), name="todo_edit"),
    path("<int:pk>/delete/", TodoDeleteView.as_view(), name="todo_delete"),
    path("<int:pk>/toggle/", TodoToggleResolvedView.as_view(), name="todo_toggle"),
]
