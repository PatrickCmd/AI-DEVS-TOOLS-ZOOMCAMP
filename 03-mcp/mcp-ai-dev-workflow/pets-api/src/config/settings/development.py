"""
Django development settings.
"""

from .base import *  # noqa: F403

# Override settings for development
DEBUG = True

# Development-specific installed apps
INSTALLED_APPS += [  # noqa: F405
    "django_extensions",  # Useful development tools
]

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Development-specific middleware
# Add debug toolbar if needed in the future
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Console email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable password validators in development for easier testing
AUTH_PASSWORD_VALIDATORS = []

# Enhanced logging for development
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# DRF - More permissive settings for development
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [  # noqa: F405
    "rest_framework.permissions.AllowAny",
]

# Show browsable API in development
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# Development-specific settings
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
