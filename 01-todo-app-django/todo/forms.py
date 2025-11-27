from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter TODO title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description (optional)",
                "rows": 4,
            }),
            "due_date": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
                "placeholder": "Select due date",
            }),
        }
        labels = {
            "title": "Title *",
            "description": "Description",
            "due_date": "Due Date & Time",
        }
