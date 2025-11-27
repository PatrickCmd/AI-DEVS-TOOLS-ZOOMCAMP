from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """
    Convert markdown text to HTML.

    Usage in templates:
    {{ todo.description|markdown }}
    """
    if not text:
        return ""

    # Configure markdown with common extensions
    return mark_safe(md.markdown(
        text,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
        ]
    ))
