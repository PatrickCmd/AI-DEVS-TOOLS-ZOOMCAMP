# Django Logging Guide

Complete guide to understanding and implementing logging in Django applications, with detailed explanations of the Petstore API logging configuration.

## Table of Contents

- [Introduction](#introduction)
- [Logging Fundamentals](#logging-fundamentals)
- [Django Logging Architecture](#django-logging-architecture)
- [Configuration Components](#configuration-components)
- [Project Logging Configuration Explained](#project-logging-configuration-explained)
- [Using Loggers in Code](#using-loggers-in-code)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

## Introduction

Logging is crucial for monitoring, debugging, and maintaining Django applications. Django uses Python's built-in `logging` module, providing a flexible and powerful logging system.

### Why Logging Matters

- **Debugging**: Track down bugs and issues in production
- **Monitoring**: Observe application behavior and performance
- **Auditing**: Keep records of important events and user actions
- **Alerting**: Get notified of critical errors
- **Analytics**: Understand usage patterns and trends

### Logging Levels

Python's logging module defines five standard severity levels:

| Level | Numeric Value | When to Use | Example |
|-------|---------------|-------------|---------|
| **DEBUG** | 10 | Detailed diagnostic information | Variable values, function calls, SQL queries |
| **INFO** | 20 | General informational messages | User login, API request, background task started |
| **WARNING** | 30 | Something unexpected but handled | Deprecated API usage, high memory usage |
| **ERROR** | 40 | Error that prevented an operation | Failed API call, database connection error |
| **CRITICAL** | 50 | Severe error, application may crash | Out of memory, critical service down |

**Log Level Hierarchy**: When you set a logger to a specific level, it captures messages at that level **and above**.

Example:
- Logger set to `INFO` captures: INFO, WARNING, ERROR, CRITICAL (but not DEBUG)
- Logger set to `ERROR` captures: ERROR, CRITICAL (but not DEBUG, INFO, WARNING)

## Logging Fundamentals

### The Four Main Components

Django logging uses four types of components that work together:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Logger    │ ───>  │   Filter    │ ───>  │   Handler   │ ───>  │  Formatter  │
│             │       │             │       │             │       │             │
│ Captures    │       │ Decides     │       │ Sends to    │       │ Formats     │
│ messages    │       │ what passes │       │ destination │       │ output      │
└─────────────┘       └─────────────┘       └─────────────┘       └─────────────┘
```

1. **Loggers**: Entry points for log messages (named instances in your code)
2. **Handlers**: Determine where log messages go (console, file, email)
3. **Filters**: Decide which log messages to process (based on conditions)
4. **Formatters**: Define the format of log message output

## Django Logging Architecture

### How Django Processes Log Messages

```python
# In your code
logger.info("User logged in")

# Flow:
# 1. Logger receives message
# 2. Checks if level >= logger's level
# 3. Passes to configured filters
# 4. If filter passes, sends to handlers
# 5. Handler checks its own level
# 6. Handler applies formatter
# 7. Handler outputs to destination (console, file, etc.)
```

### Logger Hierarchy and Propagation

Loggers are organized hierarchically using dot notation:

```
root
 ├── django
 │   ├── django.request
 │   ├── django.security
 │   ├── django.db
 │   │   └── django.db.backends
 │   └── django.template
 └── myapp
     ├── myapp.views
     │   └── myapp.views.api
     ├── myapp.models
     └── myapp.utils
```

**Propagation**: By default, messages propagate up the hierarchy:
- A message in `django.db.backends` → `django.db` → `django` → `root`
- Set `propagate: False` to stop propagation

## Configuration Components

### 1. Formatters

Formatters define how log messages appear in output.

#### Available Format Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{levelname}` | Log level name | DEBUG, INFO, ERROR |
| `{asctime}` | Human-readable time | 2025-01-04 14:30:45,123 |
| `{message}` | The log message | "User logged in" |
| `{module}` | Module name | views, models |
| `{funcName}` | Function name | login_view |
| `{lineno}` | Line number | 42 |
| `{process}` | Process ID | 12345 |
| `{thread}` | Thread ID | 67890 |
| `{pathname}` | Full file path | /app/src/users/views.py |
| `{name}` | Logger name | django.request |

#### Common Formatter Examples

**Simple Formatter** (for console):
```python
"simple": {
    "format": "{levelname} {message}",
    "style": "{"
}
# Output: INFO User logged in
```

**Verbose Formatter** (for files):
```python
"verbose": {
    "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
    "style": "{"
}
# Output: INFO 2025-01-04 14:30:45,123 views 12345 67890 User logged in
```

**Custom Formatter** (with extra context):
```python
"detailed": {
    "format": "[{asctime}] {levelname} {name} {module}:{funcName}:{lineno} - {message}",
    "style": "{",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}
# Output: [2025-01-04 14:30:45] INFO django.request views:login_view:42 - User logged in
```

**Format Styles**:
- `"{"` - Uses `{variable}` format (recommended, Python 3.2+)
- `"%"` - Uses `%(variable)s` format (old style)
- `"$"` - Uses `$variable` format

### 2. Filters

Filters provide fine-grained control over which log records are processed.

#### Built-in Django Filters

**RequireDebugTrue** - Only log when DEBUG=True:
```python
"filters": {
    "require_debug_true": {
        "()": "django.utils.log.RequireDebugTrue"
    }
}
```

**RequireDebugFalse** - Only log when DEBUG=False (production):
```python
"filters": {
    "require_debug_false": {
        "()": "django.utils.log.RequireDebugFalse"
    }
}
```

#### Custom Filter Example

```python
# myapp/logging_filters.py
import logging

class HealthCheckFilter(logging.Filter):
    """Filter out health check requests."""

    def filter(self, record):
        # Return False to discard, True to keep
        message = record.getMessage()
        return "/health/" not in message

# In settings.py
LOGGING = {
    "filters": {
        "no_health_checks": {
            "()": "myapp.logging_filters.HealthCheckFilter"
        }
    },
    "handlers": {
        "file": {
            "filters": ["no_health_checks"]
            # ...
        }
    }
}
```

### 3. Handlers

Handlers determine where log messages are sent.

#### Common Handler Classes

**StreamHandler** - Output to console (stdout/stderr):
```python
"console": {
    "class": "logging.StreamHandler",
    "level": "INFO",
    "formatter": "simple"
}
```

**FileHandler** - Write to a single file:
```python
"file": {
    "class": "logging.FileHandler",
    "filename": "/var/log/django/app.log",
    "level": "DEBUG",
    "formatter": "verbose"
}
```

**RotatingFileHandler** - Rotate files based on size:
```python
"file_rotating": {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": "/var/log/django/app.log",
    "maxBytes": 1024 * 1024 * 10,  # 10 MB
    "backupCount": 5,  # Keep 5 backup files
    "formatter": "verbose"
}
# Creates: app.log, app.log.1, app.log.2, ..., app.log.5
```

**TimedRotatingFileHandler** - Rotate files based on time:
```python
"file_timed": {
    "class": "logging.handlers.TimedRotatingFileHandler",
    "filename": "/var/log/django/app.log",
    "when": "midnight",  # Rotate at midnight
    "interval": 1,  # Every day
    "backupCount": 30,  # Keep 30 days
    "formatter": "verbose"
}
# when options: 'S' (seconds), 'M' (minutes), 'H' (hours),
#              'D' (days), 'midnight', 'W0'-'W6' (weekday)
```

**AdminEmailHandler** - Send emails to admins:
```python
"mail_admins": {
    "class": "django.utils.log.AdminEmailHandler",
    "level": "ERROR",
    "formatter": "verbose",
    "filters": ["require_debug_false"]
}
# Sends emails to addresses in ADMINS setting
```

**SysLogHandler** - Send to syslog:
```python
"syslog": {
    "class": "logging.handlers.SysLogHandler",
    "address": "/dev/log",  # Unix socket
    "facility": "local7",
    "formatter": "verbose"
}
```

### 4. Loggers

Loggers are the entry points for log messages in your code.

#### Logger Configuration

```python
"loggers": {
    "django": {
        "handlers": ["console", "file"],  # Where to send
        "level": "INFO",  # Minimum level
        "propagate": True  # Pass to parent loggers
    }
}
```

#### Important Django Loggers

| Logger Name | Purpose | When to Use |
|-------------|---------|-------------|
| `django` | General Django messages | Catch-all for Django logs |
| `django.request` | HTTP request handling | 4xx/5xx errors, request processing |
| `django.server` | Development server | Runserver output |
| `django.template` | Template rendering | Template errors and warnings |
| `django.db.backends` | Database queries | SQL query logging |
| `django.security.*` | Security events | DisallowedHost, CSRF failures |
| `django.utils.autoreload` | Auto-reloader | File change detection |

#### Root Logger

The root logger is the parent of all loggers:

```python
"root": {
    "handlers": ["console"],
    "level": "WARNING"
}
# Catches all messages not handled by specific loggers
```

## Project Logging Configuration Explained

Let's analyze the Petstore API logging configuration step by step:

### Our Configuration

```python
# src/config/settings/base.py

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR.parent / "logs" / "petstore.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
```

### Component Breakdown

#### 1. Version and Existing Loggers

```python
"version": 1,
"disable_existing_loggers": False,
```

- **version**: Always 1 (required by Python's logging.config.dictConfig)
- **disable_existing_loggers**: `False` means keep Django's default loggers active
  - If `True`, would disable all existing loggers (usually not what you want)

#### 2. Formatters

```python
"formatters": {
    "verbose": {
        "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
        "style": "{",
    },
    "simple": {
        "format": "{levelname} {message}",
        "style": "{",
    },
}
```

**Verbose Formatter** (for file logs):
- Example output: `INFO 2025-01-04 14:30:45,123 views 12345 67890 User testuser logged in`
- Includes: level, timestamp, module, process ID, thread ID, message
- Used for detailed debugging and production analysis

**Simple Formatter** (for console):
- Example output: `INFO User testuser logged in`
- Just level and message for easy reading during development

#### 3. Filters

```python
"filters": {
    "require_debug_true": {
        "()": "django.utils.log.RequireDebugTrue",
    },
}
```

- **require_debug_true**: Only passes logs when `DEBUG = True`
- Currently defined but not used in our handlers
- Can be added to console handler to prevent console spam in production

#### 4. Handlers

**Console Handler**:
```python
"console": {
    "level": "INFO",
    "class": "logging.StreamHandler",
    "formatter": "simple",
}
```

- Sends logs to console/terminal (stdout)
- Minimum level: INFO (captures INFO, WARNING, ERROR, CRITICAL)
- Uses simple formatter for readability
- Active in both development and production

**File Handler**:
```python
"file": {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": BASE_DIR.parent / "logs" / "petstore.log",
    "maxBytes": 1024 * 1024 * 10,  # 10MB
    "backupCount": 5,
    "formatter": "verbose",
}
```

- Writes to rotating log files for persistence
- **filename**: `logs/petstore.log` (relative to project root)
- **maxBytes**: 10MB - when file reaches this size, rotates to petstore.log.1
- **backupCount**: 5 - keeps petstore.log + 5 backups (petstore.log.1 through petstore.log.5)
- When 6th rotation happens, oldest (petstore.log.5) is deleted
- Uses verbose formatter for detailed information

**Log file rotation example**:
```
logs/
├── petstore.log        (current, 8MB)
├── petstore.log.1      (10MB - most recent rotation)
├── petstore.log.2      (10MB)
├── petstore.log.3      (10MB)
├── petstore.log.4      (10MB)
└── petstore.log.5      (10MB - oldest, will be deleted on next rotation)

Total storage: ~58MB maximum
```

#### 5. Root Logger

```python
"root": {
    "handlers": ["console"],
    "level": "INFO",
}
```

- Catches all log messages from any logger without specific configuration
- Sends to console only
- Minimum level: INFO
- Acts as fallback for unconfigured loggers

#### 6. Specific Loggers

**Django Logger** (general Django framework):
```python
"django": {
    "handlers": ["console", "file"],
    "level": "INFO",
    "propagate": False,
}
```

- Captures general Django framework messages
- Sends to both console and file
- Level: INFO (development messages, warnings, errors)
- `propagate: False` - doesn't pass to root logger (prevents duplicate logs)

**Django Request Logger** (HTTP requests):
```python
"django.request": {
    "handlers": ["console", "file"],
    "level": "ERROR",
    "propagate": False,
}
```

- Specifically for HTTP request/response errors
- Only logs ERROR and CRITICAL (4xx/5xx errors)
- Sends to console and file
- **Why ERROR level?** Only want to know about failed requests, not every successful request
- `propagate: False` - prevents passing to `django` logger (would duplicate)

**Apps Logger** (our application code):
```python
"apps": {
    "handlers": ["console", "file"],
    "level": "DEBUG",
    "propagate": False,
}
```

- For our application-specific logging (pets, users, store apps)
- Level: DEBUG (most verbose, captures everything)
- Sends to console and file
- Used when we name loggers: `logger = logging.getLogger('apps.pets.views')`

### Log Flow Example

When a log message is created:

```python
# In src/pets/views.py
import logging
logger = logging.getLogger('apps.pets.views')

logger.info("Creating new pet: Fluffy")
```

**Flow**:
1. Message goes to `apps.pets.views` logger
2. No specific config for `apps.pets.views`, searches up hierarchy
3. Finds `apps` logger configuration
4. Level check: INFO >= DEBUG ✓ (passes)
5. No filters applied
6. Sends to handlers: `console` and `file`
7. Console handler:
   - Level check: INFO >= INFO ✓
   - Applies simple formatter: `INFO Creating new pet: Fluffy`
   - Writes to stdout
8. File handler:
   - Level check: INFO >= INFO ✓
   - Applies verbose formatter: `INFO 2025-01-04 14:30:45,123 views 12345 67890 Creating new pet: Fluffy`
   - Writes to `logs/petstore.log`
9. `propagate: False` - stops here, doesn't send to root

## Using Loggers in Code

### Getting a Logger

Always use `__name__` to create loggers with proper namespacing:

```python
import logging

# Automatically uses module path as logger name
# e.g., 'apps.pets.views' for src/pets/views.py
logger = logging.getLogger(__name__)
```

### Logging Examples

#### In Views

```python
# src/pets/views.py
import logging
from rest_framework import viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class PetViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating pet: {request.data.get('name')}")

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pet = serializer.save()

            logger.info(f"Pet created successfully: {pet.id}")
            return Response(serializer.data, status=201)

        except Exception as e:
            logger.error(
                f"Failed to create pet: {str(e)}",
                exc_info=True  # Include stack trace
            )
            raise
```

#### In Models

```python
# src/pets/models.py
import logging
from django.db import models

logger = logging.getLogger(__name__)

class Pet(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            logger.debug(f"Creating new pet: {self.name}")
        else:
            logger.debug(f"Updating pet {self.pk}: {self.name}")

        super().save(*args, **kwargs)

        if is_new:
            logger.info(f"Pet {self.pk} created: {self.name}")
```

#### Different Log Levels

```python
# DEBUG: Detailed diagnostic info
logger.debug(f"User {user.id} session data: {session_data}")

# INFO: Informational messages
logger.info(f"User {user.username} logged in from {request.META['REMOTE_ADDR']}")

# WARNING: Unexpected but handled
logger.warning(f"User {user.username} attempted to access restricted resource")

# ERROR: Error that prevented operation
logger.error(f"Failed to send email to {user.email}: {str(exception)}")

# CRITICAL: Severe error
logger.critical("Database connection lost - application may be unstable")
```

#### Logging Exceptions

```python
try:
    # Some operation
    result = external_api_call()
except APIException as e:
    # Log with automatic stack trace
    logger.exception("API call failed")
    # Same as: logger.error("API call failed", exc_info=True)

except ValueError as e:
    # Log without stack trace
    logger.error(f"Invalid value: {e}")
```

#### Structured Logging with Extra Context

```python
logger.info(
    "User action completed",
    extra={
        "user_id": request.user.id,
        "action": "purchase",
        "amount": 99.99,
        "ip_address": request.META.get('REMOTE_ADDR')
    }
)
```

### Logger Naming Strategy

Use hierarchical naming for organization:

```python
# Good: Hierarchical naming
logger = logging.getLogger(__name__)
# Results in: 'apps.pets.views', 'apps.pets.models', etc.

# Avoid: Random names
logger = logging.getLogger('mylogger')  # Hard to organize

# App-specific loggers
pets_logger = logging.getLogger('apps.pets')
users_logger = logging.getLogger('apps.users')
store_logger = logging.getLogger('apps.store')

# Feature-specific
payment_logger = logging.getLogger('apps.store.payment')
auth_logger = logging.getLogger('apps.users.auth')
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# ✓ Good
logger.debug(f"SQL query: {query}")  # Detailed debugging
logger.info("User registered")  # Notable events
logger.warning("Deprecated API used")  # Potential issues
logger.error("Payment failed")  # Actual errors
logger.critical("Database down")  # Severe problems

# ✗ Avoid
logger.error("User logged in")  # This is INFO
logger.info("Database connection failed")  # This is ERROR
```

### 2. Include Context in Messages

```python
# ✓ Good - Includes context
logger.error(
    f"Failed to create order for user {user.id}: {str(e)}",
    extra={
        "user_id": user.id,
        "items": item_count,
        "total": order_total
    }
)

# ✗ Avoid - Vague
logger.error("Order creation failed")
```

### 3. Don't Log Sensitive Data

```python
# ✗ NEVER log sensitive data
logger.info(f"User password: {password}")  # SECURITY RISK!
logger.debug(f"Credit card: {card_number}")  # SECURITY RISK!
logger.info(f"API key: {api_key}")  # SECURITY RISK!

# ✓ Good - Log safely
logger.info(f"User {user.username} authenticated")
logger.debug(f"Payment processed for user {user.id}")
logger.info(f"API request to {endpoint}")
```

### 4. Use exc_info for Exceptions

```python
# ✓ Good - Includes stack trace
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
    # Or use logger.exception() which does this automatically
    logger.exception("Operation failed")

# ✗ Avoid - Missing context
try:
    risky_operation()
except Exception as e:
    logger.error(str(e))  # No stack trace
```

### 5. Configure Different Settings per Environment

```python
# config/settings/development.py
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # Verbose in dev

# config/settings/production.py
LOGGING["loggers"]["apps"]["level"] = "INFO"  # Less verbose in prod
LOGGING["handlers"]["mail_admins"] = {  # Email errors
    "class": "django.utils.log.AdminEmailHandler",
    "level": "ERROR",
}
```

### 6. Don't Log in Settings.py

```python
# ✗ AVOID - Logging not set up yet
# settings.py
logger = logging.getLogger(__name__)
logger.info("Settings loaded")  # Won't work properly

# ✓ Good - Log in views, models, etc.
# views.py
logger = logging.getLogger(__name__)
logger.info("View called")  # Works correctly
```

### 7. Use Lazy Formatting

```python
# ✓ Good - Only formats if logged
logger.debug("User %s performed action %s", user.id, action)

# ✗ Avoid - Always formats even if not logged
logger.debug(f"User {user.id} performed action {action}")
# If DEBUG is disabled, still does string formatting unnecessarily
```

## Common Patterns

### Pattern 1: Request/Response Logging Middleware

```python
# middleware/logging_middleware.py
import logging
import time

logger = logging.getLogger('apps.middleware')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request
        start_time = time.time()
        logger.info(
            f"Request: {request.method} {request.path}",
            extra={
                "method": request.method,
                "path": request.path,
                "user": getattr(request.user, 'id', None),
                "ip": request.META.get('REMOTE_ADDR')
            }
        )

        # Process request
        response = self.get_response(request)

        # Log response
        duration = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} ({duration:.2f}s)",
            extra={
                "status": response.status_code,
                "duration": duration,
                "path": request.path
            }
        )

        return response
```

### Pattern 2: Database Query Logging

```python
# Enable in development to see SQL queries
LOGGING = {
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",  # Shows all SQL queries
            "propagate": False,
        },
    },
}
```

### Pattern 3: Separate Log Files per App

```python
LOGGING = {
    "handlers": {
        "pets_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/pets.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 3,
        },
        "users_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/users.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 3,
        },
    },
    "loggers": {
        "apps.pets": {
            "handlers": ["console", "pets_file"],
            "level": "DEBUG",
        },
        "apps.users": {
            "handlers": ["console", "users_file"],
            "level": "DEBUG",
        },
    },
}
```

### Pattern 4: Performance Logging Decorator

```python
import logging
import time
from functools import wraps

logger = logging.getLogger('apps.performance')

def log_performance(func):
    """Decorator to log function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        logger.debug(f"Starting {func.__name__}")

        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(
                f"{func.__name__} completed in {duration:.3f}s",
                extra={"function": func.__name__, "duration": duration}
            )
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(
                f"{func.__name__} failed after {duration:.3f}s: {e}",
                exc_info=True
            )
            raise

    return wrapper

# Usage
@log_performance
def expensive_operation():
    # ... complex logic
    pass
```

### Pattern 5: Audit Logging

```python
# apps/common/audit_logger.py
import logging

audit_logger = logging.getLogger('apps.audit')

def log_user_action(user, action, resource, details=None):
    """Log user actions for auditing."""
    audit_logger.info(
        f"User {user.username} {action} {resource}",
        extra={
            "user_id": user.id,
            "username": user.username,
            "action": action,
            "resource": resource,
            "details": details or {},
            "timestamp": timezone.now().isoformat(),
        }
    )

# Usage in views
from apps.common.audit_logger import log_user_action

def delete_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    log_user_action(
        user=request.user,
        action="DELETE",
        resource=f"Pet:{pet.id}",
        details={"pet_name": pet.name}
    )
    pet.delete()
```

## Troubleshooting

### Issue 1: Logs Not Appearing

**Problem**: Logger configured but no output

**Solutions**:

```python
# Check 1: Logger level too high
"loggers": {
    "apps": {
        "level": "ERROR"  # Won't show INFO messages
    }
}
# Fix: Lower the level
"loggers": {
    "apps": {
        "level": "DEBUG"  # Shows all messages
    }
}

# Check 2: Handler level too high
"handlers": {
    "console": {
        "level": "WARNING"  # Won't show INFO
    }
}
# Fix: Lower handler level
"handlers": {
    "console": {
        "level": "DEBUG"
    }
}

# Check 3: Wrong logger name
logger = logging.getLogger('wrong.name')  # Not in config
# Fix: Use configured logger name
logger = logging.getLogger('apps.pets')  # Matches config
```

### Issue 2: Duplicate Log Messages

**Problem**: Same message appears multiple times

**Cause**: Propagation causing messages to be handled by multiple loggers

```python
# Problem configuration
"loggers": {
    "apps": {
        "handlers": ["console", "file"],
        "propagate": True  # ← Causes duplicates
    }
}
"root": {
    "handlers": ["console"]  # ← Also logs same message
}

# Fix: Disable propagation
"loggers": {
    "apps": {
        "handlers": ["console", "file"],
        "propagate": False  # ← Stops here
    }
}
```

### Issue 3: Permission Denied for Log File

**Problem**: Can't write to log file

```bash
PermissionError: [Errno 13] Permission denied: '/var/log/django/app.log'
```

**Solutions**:

```bash
# Option 1: Create logs directory with correct permissions
mkdir -p logs
chmod 755 logs

# Option 2: Use relative path (recommended in Docker)
# In settings.py
"filename": BASE_DIR.parent / "logs" / "petstore.log"

# Option 3: Ensure logs directory exists in Dockerfile
RUN mkdir -p /app/logs && chmod 755 /app/logs
```

### Issue 4: Log Files Growing Too Large

**Problem**: Log files consuming too much disk space

**Solutions**:

```python
# Solution 1: Use RotatingFileHandler
"handlers": {
    "file": {
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10 MB
        "backupCount": 5  # Keep only 5 old files
    }
}

# Solution 2: Use TimedRotatingFileHandler
"handlers": {
    "file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "when": "midnight",
        "interval": 1,
        "backupCount": 7  # Keep 7 days
    }
}

# Solution 3: Increase log level in production
# development.py
LOGGING["loggers"]["apps"]["level"] = "DEBUG"

# production.py
LOGGING["loggers"]["apps"]["level"] = "WARNING"  # Less verbose
```

### Issue 5: Sensitive Data in Logs

**Problem**: Accidentally logging passwords, API keys, etc.

**Prevention**:

```python
# Create a sanitizing filter
class SanitizeFilter(logging.Filter):
    def filter(self, record):
        # Sanitize message
        record.msg = self.sanitize(record.msg)
        return True

    def sanitize(self, message):
        import re
        # Remove patterns that look like passwords, keys, etc.
        message = re.sub(r'password["\']?\s*[:=]\s*["\']?[\w@#$%]+',
                        'password=***', message, flags=re.I)
        message = re.sub(r'api[_-]?key["\']?\s*[:=]\s*["\']?[\w-]+',
                        'api_key=***', message, flags=re.I)
        return message

# Add to configuration
LOGGING = {
    "filters": {
        "sanitize": {
            "()": "myapp.logging_filters.SanitizeFilter"
        }
    },
    "handlers": {
        "file": {
            "filters": ["sanitize"]
        }
    }
}
```

## Advanced Topics

### JSON Logging for Production

For easier parsing and analysis:

```python
# Install: pip install python-json-logger

LOGGING = {
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "json_file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.json",
            "formatter": "json"
        }
    }
}

# Output:
# {"asctime": "2025-01-04 14:30:45,123", "name": "apps.pets",
#  "levelname": "INFO", "message": "Pet created"}
```

### Logging to External Services

**Sentry Integration**:

```python
# Install: pip install sentry-sdk

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration(), sentry_logging],
    traces_sample_rate=1.0,
)
```

### Logging Best Practices Checklist

- [ ] Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- [ ] Include context in log messages (user ID, request ID, etc.)
- [ ] Never log sensitive data (passwords, API keys, credit cards)
- [ ] Use `exc_info=True` or `logger.exception()` for exceptions
- [ ] Configure different log levels for development vs production
- [ ] Use rotating file handlers to prevent disk space issues
- [ ] Implement structured logging (JSON) for production
- [ ] Set up alerts for CRITICAL and ERROR logs
- [ ] Use hierarchical logger names (`__name__`)
- [ ] Set `propagate=False` to avoid duplicate logs
- [ ] Don't log in settings.py (logging not configured yet)
- [ ] Use lazy formatting for performance
- [ ] Test logging configuration in all environments

## Quick Reference

### Common Configuration Snippets

**Basic Console Logging**:
```python
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {"class": "logging.StreamHandler"}
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}
```

**File + Console Logging**:
```python
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO"
    }
}
```

**Production Setup (Email Errors)**:
```python
LOGGING = {
    "version": 1,
    "handlers": {
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
            "filters": ["require_debug_false"]
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR"
        }
    }
}

ADMINS = [("Admin", "admin@example.com")]
```

## Resources

- [Django Logging Documentation](https://docs.djangoproject.com/en/5.2/topics/logging/)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Logging Best Practices](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

---

**Last Updated**: January 2026
