from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm


class TodoListView(ListView):
    model = Todo
    template_name = "home.html"
    context_object_name = "todos"


class TodoCreateView(CreateView):
    model = Todo
    template_name = "todo_form.html"
    form_class = TodoForm
    success_url = reverse_lazy("todo_list")


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todo_form.html"
    form_class = TodoForm
    success_url = reverse_lazy("todo_list")


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todo_confirm_delete.html"
    success_url = reverse_lazy("todo_list")


class TodoToggleResolvedView(View):
    def post(self, _request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.is_resolved = not todo.is_resolved
        todo.save()
        return redirect("todo_list")
