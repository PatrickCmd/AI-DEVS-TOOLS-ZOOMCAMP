"""
Django production settings.
"""

from .base import *  # noqa: F403

# Production settings
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Production allowed hosts should be set via environment variables
# ALLOWED_HOSTS is already set from base.py via env_settings

# Production logging - log to file and console
LOGGING["handlers"]["console"]["level"] = "WARNING"  # noqa: F405
LOGGING["handlers"]["file"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "INFO"  # noqa: F405

# Email backend for production (configure SMTP settings via environment)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env_settings.get("EMAIL_HOST", "localhost")  # noqa: F405
EMAIL_PORT = env_settings.get("EMAIL_PORT", 587)  # noqa: F405
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env_settings.get("EMAIL_HOST_USER", "")  # noqa: F405
EMAIL_HOST_PASSWORD = env_settings.get("EMAIL_HOST_PASSWORD", "")  # noqa: F405

# Production cache (can be Redis)
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": env_settings.redis_url,
#     }
# }

# Disable browsable API in production
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]

# Production permission classes
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [  # noqa: F405
    "rest_framework.permissions.IsAuthenticatedOrReadOnly",
]
