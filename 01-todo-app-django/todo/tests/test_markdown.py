import pytest
from django.template import Context, Template
from todo.models import Todo


@pytest.mark.django_db
class TestMarkdownRendering:
    def test_markdown_filter_basic(self):
        """Test basic markdown rendering"""
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": "**bold** and *italic*"})
        result = template.render(context)
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_markdown_filter_empty_string(self):
        """Test markdown filter with empty string"""
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": ""})
        result = template.render(context)
        assert result == ""

    def test_markdown_filter_none(self):
        """Test markdown filter with None value"""
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": None})
        result = template.render(context)
        assert result == ""

    def test_markdown_filter_with_lists(self):
        """Test markdown rendering with lists"""
        text = "- Item 1\n- Item 2\n- Item 3"
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": text})
        result = template.render(context)
        assert "<ul>" in result
        assert "<li>Item 1</li>" in result

    def test_markdown_filter_with_code(self):
        """Test markdown rendering with inline code"""
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": "Use `print()` function"})
        result = template.render(context)
        assert "<code>print()</code>" in result

    def test_markdown_filter_with_links(self):
        """Test markdown rendering with links"""
        template = Template("{% load markdown_extras %}{{ text|markdown }}")
        context = Context({"text": "[Google](https://google.com)"})
        result = template.render(context)
        assert '<a href="https://google.com">Google</a>' in result

    def test_markdown_in_todo_list_view(self, client):
        """Test that markdown is rendered in the list view"""
        Todo.objects.create(
            title="Markdown Test",
            description="**Bold text** and *italic text*"
        )
        response = client.get("/")
        content = response.content.decode()
        assert "<strong>Bold text</strong>" in content
        assert "<em>italic text</em>" in content

    def test_markdown_with_headers(self, client):
        """Test markdown headers in todo description"""
        Todo.objects.create(
            title="Header Test",
            description="## Subtitle\nThis is content"
        )
        response = client.get("/")
        content = response.content.decode()
        assert "<h2>Subtitle</h2>" in content

    def test_markdown_with_code_block(self, client):
        """Test markdown code blocks"""
        Todo.objects.create(
            title="Code Test",
            description="```python\nprint('hello')\n```"
        )
        response = client.get("/")
        content = response.content.decode()
        assert "<pre>" in content
        assert "<code>" in content
        # Check for either escaped or unescaped version
        assert "print" in content and "hello" in content
