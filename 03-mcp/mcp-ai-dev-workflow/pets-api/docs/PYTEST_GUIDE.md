# Pytest Guide: Fixtures, Scopes, and Django Integration

Comprehensive guide to using pytest with Django, covering fixtures, scopes, configuration, and best practices for the Petstore API project.

## Table of Contents

- [Introduction](#introduction)
- [Pytest Basics](#pytest-basics)
- [Fixtures Fundamentals](#fixtures-fundamentals)
- [Fixture Scopes](#fixture-scopes)
- [conftest.py and Fixture Discovery](#conftestpy-and-fixture-discovery)
- [Django Integration](#django-integration)
- [Project-Specific Fixtures](#project-specific-fixtures)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

## Introduction

Pytest is a mature, feature-rich testing framework that makes it easy to write simple, scalable, and maintainable tests. This guide focuses on using pytest with Django for the Petstore API project.

### Why Pytest?

- **Simple syntax**: No boilerplate, just plain `assert` statements
- **Powerful fixtures**: Reusable setup and teardown code
- **Excellent plugin ecosystem**: Including `pytest-django` for Django integration
- **Detailed failure reports**: Clear information when tests fail
- **Parallel execution**: Run tests faster with `pytest-xdist`
- **Parametrization**: Easily run the same test with different inputs

## Pytest Basics

### Writing a Simple Test

```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string_operations():
    text = "hello world"
    assert text.startswith("hello")
    assert "world" in text
    assert text.upper() == "HELLO WORLD"
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
docker compose exec backend pytest src/pets/tests/test_models.py

# Run specific test function
docker compose exec backend pytest src/pets/tests/test_models.py::test_create_category

# Run with verbose output
docker compose exec backend pytest src/ -v

# Run with coverage
make test-cov
```

## Fixtures Fundamentals

Fixtures are functions that provide data, setup, or teardown to tests. They promote code reuse and make tests more maintainable.

### Basic Fixture Definition

```python
import pytest

@pytest.fixture
def sample_user():
    """Provide a sample user dictionary."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test"
    }

def test_user_data(sample_user):
    """Test receives fixture as an argument."""
    assert sample_user["username"] == "testuser"
    assert "@" in sample_user["email"]
```

### Fixtures with Setup and Teardown

Use `yield` to separate setup from teardown:

```python
@pytest.fixture
def smtp_connection():
    """Create SMTP connection with cleanup."""
    # Setup: runs before test
    import smtplib
    connection = smtplib.SMTP("smtp.example.com", 587)

    yield connection  # Provide to test

    # Teardown: runs after test (even if test fails)
    connection.close()

def test_send_email(smtp_connection):
    """Use the connection fixture."""
    smtp_connection.ehlo()
    assert smtp_connection.helo_resp
```

### Fixture Parameters

The `@pytest.fixture` decorator accepts several parameters:

```python
@pytest.fixture(
    scope="function",      # Scope: function, class, module, package, session
    params=None,           # List of parameters for parameterized fixtures
    autouse=False,         # Auto-use for all tests in scope
    ids=None,              # Custom IDs for parameterized fixtures
    name=None              # Custom fixture name
)
def my_fixture():
    pass
```

## Fixture Scopes

Scopes determine how often a fixture is instantiated and shared across tests.

### Available Scopes

| Scope | Description | Lifetime | Use Case |
|-------|-------------|----------|----------|
| **function** | Default scope | Per test function | Test-specific data, most common |
| **class** | Per test class | All tests in a class | Shared setup for related tests |
| **module** | Per test module | All tests in a file | Expensive resources shared in file |
| **package** | Per test package | All tests in package | Package-level shared resources |
| **session** | Per test session | Entire test run | Database connections, global config |

### Function Scope (Default)

Created for each test function. Most common and safest scope.

```python
@pytest.fixture  # scope="function" is default
def user():
    """Create a fresh user for each test."""
    return User.objects.create(username="testuser")

def test_user_creation(user):
    assert user.username == "testuser"

def test_user_modification(user):
    # Gets a NEW user instance, not the one from test_user_creation
    user.username = "modified"
    assert user.username == "modified"
```

### Class Scope

Shared across all test methods in a class.

```python
@pytest.fixture(scope="class")
def database_connection():
    """Single DB connection for all tests in class."""
    conn = create_connection()
    yield conn
    conn.close()

class TestDatabase:
    def test_read(self, database_connection):
        # Uses same connection
        pass

    def test_write(self, database_connection):
        # Uses same connection as test_read
        pass
```

### Module Scope

Shared across all tests in a module (file).

```python
@pytest.fixture(scope="module")
def api_client():
    """Single API client for entire module."""
    client = APIClient()
    # Expensive setup
    client.authenticate()
    return client

def test_endpoint_1(api_client):
    # Shares client with other tests
    pass

def test_endpoint_2(api_client):
    # Same client instance
    pass
```

### Session Scope

Created once for the entire test session. Most efficient but requires careful management.

```python
@pytest.fixture(scope="session")
def base_configuration():
    """Load configuration once for all tests."""
    config = load_config_from_file()
    return config
```

### Scope Execution Order

Higher-scoped fixtures run before lower-scoped ones:

```python
@pytest.fixture(scope="session")
def order():
    return []

@pytest.fixture(scope="session")
def sess(order):
    order.append("session")

@pytest.fixture(scope="package")
def pack(order):
    order.append("package")

@pytest.fixture(scope="module")
def mod(order):
    order.append("module")

@pytest.fixture(scope="class")
def cls(order):
    order.append("class")

@pytest.fixture
def func(order):
    order.append("function")

class TestClass:
    def test_order(self, func, cls, mod, pack, sess, order):
        # Execution order: session → package → module → class → function
        assert order == ["session", "package", "module", "class", "function"]
```

## conftest.py and Fixture Discovery

### What is conftest.py?

`conftest.py` is a special pytest file that:
- Provides fixtures to all tests in its directory and subdirectories
- Automatically discovered by pytest (no imports needed)
- Can exist at multiple levels in your test hierarchy
- Can define plugins and hooks

### Fixture Discovery Rules

1. **Search Upward**: Tests search upward through parent directories for fixtures
2. **Never Search Down**: Tests cannot access fixtures in child directories
3. **First Match Wins**: The first fixture found is used
4. **Override by Redefining**: Child conftest.py can override parent fixtures

### Directory Structure Example

```
project/
├── conftest.py              # Root fixtures (available to all tests)
├── tests/
│   ├── conftest.py          # Test-wide fixtures
│   ├── test_basic.py
│   ├── pets/
│   │   ├── conftest.py      # Pet-specific fixtures
│   │   ├── test_models.py
│   │   └── test_views.py
│   └── users/
│       ├── conftest.py      # User-specific fixtures
│       └── test_views.py
```

### Sharing Fixtures Across Files

**Root conftest.py** (src/conftest.py):

```python
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Provide API client to all tests."""
    return APIClient()

@pytest.fixture
def user(db):
    """Create a test user available to all tests."""
    from users.models import User
    return User.objects.create(
        username="testuser",
        email="test@example.com"
    )
```

**Tests automatically discover these fixtures**:

```python
# src/pets/tests/test_views.py
# No imports needed!

def test_list_pets(api_client):
    """api_client fixture automatically available."""
    response = api_client.get("/v2/pet/")
    assert response.status_code == 200
```

### Overriding Fixtures in Subdirectories

**Parent conftest.py**:

```python
# tests/conftest.py
@pytest.fixture
def username():
    return "defaultuser"
```

**Child conftest.py**:

```python
# tests/subfolder/conftest.py
@pytest.fixture
def username(username):
    """Override and extend parent fixture."""
    return f"overridden-{username}"

def test_username(username):
    assert username == "overridden-defaultuser"
```

### Using Fixtures from External Projects

Register external fixtures in conftest.py:

```python
# conftest.py
pytest_plugins = [
    "mylibrary.fixtures",
    "another_package.test_helpers"
]
```

## Django Integration

### Installing pytest-django

Already included in the project:

```toml
# pyproject.toml
[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-django>=4.9.0",
    # ...
]
```

### The @pytest.mark.django_db Decorator

**Required for database access**. Django tests need explicit permission to access the database.

```python
import pytest
from users.models import User

@pytest.mark.django_db
def test_create_user():
    """Mark required for database access."""
    user = User.objects.create(username="testuser")
    assert user.username == "testuser"
```

### Marking Entire Test Classes

```python
@pytest.mark.django_db
class TestUserModel:
    """All methods have database access."""

    def test_create_user(self):
        user = User.objects.create(username="testuser")
        assert user.pk is not None

    def test_user_count(self):
        User.objects.create(username="user1")
        User.objects.create(username="user2")
        assert User.objects.count() == 2
```

### Marking Entire Modules

```python
# At top of test file
pytestmark = pytest.mark.django_db

# All tests in this module now have database access
def test_1():
    pass

def test_2():
    pass
```

### Transactional Tests

By default, pytest-django wraps each test in a transaction. For testing transactions explicitly:

```python
@pytest.mark.django_db(transaction=True)
def test_transaction_behavior():
    """Test with transaction support."""
    from django.db import transaction

    user = User.objects.create(username="testuser")

    try:
        with transaction.atomic():
            user.username = "modified"
            user.save()
            raise Exception("Rollback!")
    except Exception:
        pass

    user.refresh_from_db()
    assert user.username == "testuser"  # Rolled back
```

### Built-in Django Fixtures

#### client

Django test client for making requests:

```python
def test_homepage(client):
    """client fixture provided by pytest-django."""
    response = client.get("/")
    assert response.status_code == 200
```

#### admin_client

Pre-authenticated admin client:

```python
def test_admin_page(admin_client):
    """Admin client is already logged in."""
    response = admin_client.get("/admin/")
    assert response.status_code == 200
```

#### db

Provides database access without using the marker:

```python
def test_with_db_fixture(db):
    """db fixture gives database access."""
    user = User.objects.create(username="testuser")
    assert User.objects.count() == 1
```

#### django_user_model

Access the User model:

```python
def test_user_model(django_user_model):
    """Get User model dynamically."""
    user = django_user_model.objects.create(username="test")
    assert user.pk is not None
```

#### settings

Modify Django settings for a test:

```python
def test_with_custom_setting(settings):
    """Temporarily change settings."""
    settings.DEBUG = True
    settings.ALLOWED_HOSTS = ["testserver"]
    # Changes only apply to this test
```

#### live_server

Start a live Django server for integration tests:

```python
@pytest.mark.django_db
def test_live_server(live_server):
    """Test against a live server."""
    import requests
    response = requests.get(f"{live_server.url}/api/")
    assert response.status_code == 200
```

## Project-Specific Fixtures

### Our Current Fixtures (src/conftest.py)

```python
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from pets.models import Category, Pet, Tag
from store.models import Order

User = get_user_model()


@pytest.fixture
def api_client():
    """Provide DRF API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone="1234567890"
    )


@pytest.fixture
def authenticated_client(api_client, user_tokens):
    """Provide authenticated API client."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
    return api_client


@pytest.fixture
def user_tokens(user):
    """Generate JWT tokens for test user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(name="Dogs")


@pytest.fixture
def tag(db):
    """Create a test tag."""
    return Tag.objects.create(name="friendly")


@pytest.fixture
def pet(db, category):
    """Create a test pet."""
    return Pet.objects.create(
        name="Fluffy",
        category=category,
        status="available",
        photo_urls=["http://example.com/fluffy.jpg"]
    )


@pytest.fixture
def order(db, pet, user):
    """Create a test order."""
    return Order.objects.create(
        pet=pet,
        user=user,
        quantity=1,
        status="placed"
    )
```

### Using Project Fixtures

```python
# src/pets/tests/test_views.py

def test_create_pet_authenticated(authenticated_client, category):
    """Uses authenticated_client and category fixtures."""
    data = {
        "name": "Max",
        "category": category.id,
        "status": "available"
    }
    response = authenticated_client.post("/v2/pet/", data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Max"


def test_list_pets_with_data(api_client, pet):
    """Uses api_client and pet fixtures."""
    response = api_client.get("/v2/pet/")
    assert response.status_code == 200
    assert len(response.data["results"]) >= 1
```

## Configuration

### pyproject.toml Configuration

Our current pytest configuration:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--reuse-db",
    "--nomigrations",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing:skip-covered",
    "--strict-markers",
]
testpaths = ["src"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

### Configuration Options Explained

#### DJANGO_SETTINGS_MODULE
Specifies which Django settings to use for tests:

```toml
DJANGO_SETTINGS_MODULE = "config.settings.test"
```

#### python_files
Patterns for test file discovery:

```toml
python_files = ["test_*.py", "*_test.py"]
```

#### python_classes
Patterns for test class discovery:

```toml
python_classes = ["Test*"]
```

#### python_functions
Patterns for test function discovery:

```toml
python_functions = ["test_*"]
```

#### addopts
Command-line options to always use:

```toml
addopts = [
    "--reuse-db",           # Reuse database between test runs (faster)
    "--nomigrations",       # Don't run migrations (use --create-db when needed)
    "--cov=src",            # Coverage for src directory
    "--cov-report=html",    # Generate HTML coverage report
    "--strict-markers",     # Raise errors for unknown markers
]
```

#### testpaths
Directories to search for tests:

```toml
testpaths = ["src"]
```

#### markers
Custom markers for organizing tests:

```toml
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

**Using markers**:

```python
@pytest.mark.slow
def test_expensive_operation():
    pass

@pytest.mark.integration
def test_api_integration():
    pass
```

**Running specific markers**:

```bash
# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"

# Run integration tests
pytest -m integration
```

## Best Practices

### 1. Use Appropriate Scopes

- **function**: Default, safest, most isolated
- **class**: Group related tests
- **module**: Expensive resources shared in file
- **session**: Global resources (use sparingly)

```python
# Good: Function scope for test data
@pytest.fixture
def user():
    return User.objects.create(username="testuser")

# Good: Session scope for expensive setup
@pytest.fixture(scope="session")
def django_db_setup():
    # One-time database configuration
    pass
```

### 2. Keep Fixtures Simple and Focused

```python
# Good: Single responsibility
@pytest.fixture
def user():
    return User.objects.create(username="testuser")

@pytest.fixture
def authenticated_client(api_client, user):
    client = api_client
    client.force_authenticate(user=user)
    return client

# Avoid: Doing too much in one fixture
@pytest.fixture
def everything():
    user = create_user()
    client = setup_client()
    authenticate(client, user)
    create_test_data()
    # ... too much
```

### 3. Use Explicit Database Markers

```python
# Good: Explicit marker
@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(username="test")
    assert user.pk

# Good: Using db fixture
def test_user_query(db):
    assert User.objects.count() == 0
```

### 4. Organize Fixtures by Scope

```python
# conftest.py structure
# Session-scoped fixtures first
@pytest.fixture(scope="session")
def base_config():
    pass

# Module-scoped fixtures
@pytest.fixture(scope="module")
def api_client():
    pass

# Function-scoped fixtures (default)
@pytest.fixture
def user():
    pass
```

### 5. Use Fixture Dependencies

```python
@pytest.fixture
def category():
    return Category.objects.create(name="Dogs")

@pytest.fixture
def pet(category):  # Depends on category
    return Pet.objects.create(
        name="Fluffy",
        category=category
    )

@pytest.fixture
def order(pet, user):  # Depends on pet and user
    return Order.objects.create(pet=pet, user=user)
```

### 6. Use autouse Sparingly

```python
# Good use case: Setup needed for all tests
@pytest.fixture(autouse=True)
def reset_cache():
    """Clear cache before each test."""
    cache.clear()

# Avoid: Auto-use when not all tests need it
@pytest.fixture(autouse=True)  # Bad if not all tests need DB
def create_test_data():
    User.objects.create(username="admin")
```

### 7. Name Fixtures Descriptively

```python
# Good
@pytest.fixture
def authenticated_admin_client():
    pass

@pytest.fixture
def published_blog_post():
    pass

# Avoid
@pytest.fixture
def client1():
    pass

@pytest.fixture
def data():
    pass
```

## Common Patterns

### Pattern 1: Factory Fixtures

Create multiple instances:

```python
@pytest.fixture
def user_factory(db):
    """Factory for creating users."""
    def create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        defaults.update(kwargs)
        return User.objects.create(**defaults)
    return create_user

def test_multiple_users(user_factory):
    user1 = user_factory(username="user1")
    user2 = user_factory(username="user2")
    assert User.objects.count() == 2
```

### Pattern 2: Parametrized Fixtures

Test with multiple configurations:

```python
@pytest.fixture(params=["available", "pending", "sold"])
def pet_status(request):
    """Fixture runs test 3 times with different statuses."""
    return request.param

def test_pet_status_filter(api_client, pet_status):
    """Runs 3 times: available, pending, sold."""
    response = api_client.get(f"/v2/pet/findByStatus?status={pet_status}")
    assert response.status_code == 200
```

### Pattern 3: Fixture with Cleanup

```python
@pytest.fixture
def temp_file():
    """Create temporary file with cleanup."""
    import tempfile

    fd, path = tempfile.mkstemp()

    yield path  # Provide to test

    # Cleanup
    import os
    os.close(fd)
    os.unlink(path)
```

### Pattern 4: Request Fixture for Dynamic Behavior

```python
@pytest.fixture
def user(request, db):
    """Create user with optional superuser status."""
    is_superuser = getattr(request, "param", False)

    if is_superuser:
        return User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="test123"
    )

# Use with indirect parametrization
@pytest.mark.parametrize("user", [False, True], indirect=True)
def test_user_permissions(user):
    if user.is_superuser:
        assert user.has_perm("any.permission")
```

### Pattern 5: Combining Multiple Fixtures

```python
@pytest.fixture
def complete_order_setup(db, user, pet):
    """Combine multiple fixtures for complex setup."""
    order = Order.objects.create(
        pet=pet,
        user=user,
        quantity=5,
        status="approved",
        complete=True
    )
    return {
        "user": user,
        "pet": pet,
        "order": order
    }

def test_order_completion(complete_order_setup):
    order = complete_order_setup["order"]
    assert order.complete is True
    assert order.quantity == 5
```

## Troubleshooting

### Issue 1: "Database access not allowed"

**Error**:
```
django.db.utils.ProgrammingError: Database access not allowed
```

**Solution**: Add `@pytest.mark.django_db` or use `db` fixture:

```python
# Option 1: Use decorator
@pytest.mark.django_db
def test_user():
    User.objects.create(username="test")

# Option 2: Use db fixture
def test_user(db):
    User.objects.create(username="test")
```

### Issue 2: Fixtures Not Found

**Error**:
```
fixture 'my_fixture' not found
```

**Solution**: Check fixture discovery:

1. Ensure fixture is in `conftest.py` in current or parent directory
2. Check fixture name spelling
3. Verify conftest.py is valid Python

```python
# conftest.py must be in test path
tests/
├── conftest.py  ← Fixtures here
└── test_views.py  ← Can use fixtures
```

### Issue 3: Test Database Not Created

**Error**:
```
django.db.utils.OperationalError: database "test_db" does not exist
```

**Solution**: Run with `--create-db` once:

```bash
docker compose exec backend pytest --create-db
```

### Issue 4: Fixture Scope Mismatch

**Error**:
```
ScopeMismatch: Cannot use function-scoped fixture in session-scoped fixture
```

**Solution**: Match or increase fixture scopes:

```python
# Bad: session fixture using function-scoped db
@pytest.fixture(scope="session")
def data(db):  # db is function-scoped
    pass

# Good: Match scopes
@pytest.fixture(scope="session")
def data(django_db_setup):  # session-scoped
    pass
```

### Issue 5: Slow Tests

**Solution**: Use `--reuse-db` and `--nomigrations`:

```bash
# In pyproject.toml
addopts = ["--reuse-db", "--nomigrations"]

# When you need to recreate DB
pytest --create-db
```

### Issue 6: Fixture Teardown Not Running

**Issue**: Cleanup code after `yield` not executing

**Solution**: Ensure test completes (doesn't hang) and use try/finally if needed:

```python
@pytest.fixture
def resource():
    res = setup_resource()
    try:
        yield res
    finally:
        # Guaranteed cleanup
        res.cleanup()
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Guide](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Real Python: Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)

## Quick Reference

### Common Commands

```bash
# Run all tests
make test

# Run specific app tests
make test-pets
make test-users
make test-store

# Run with coverage
make test-cov

# Run specific test file
pytest src/pets/tests/test_models.py

# Run specific test function
pytest src/pets/tests/test_models.py::test_create_pet

# Run tests matching pattern
pytest -k "test_user"

# Run with markers
pytest -m "not slow"

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Debug with pdb
pytest --pdb
```

### Fixture Quick Reference

```python
# Basic fixture
@pytest.fixture
def data():
    return {"key": "value"}

# Fixture with setup/teardown
@pytest.fixture
def resource():
    res = setup()
    yield res
    cleanup(res)

# Scoped fixture
@pytest.fixture(scope="module")
def expensive_resource():
    return create_expensive_resource()

# Autouse fixture
@pytest.fixture(autouse=True)
def reset_state():
    State.reset()

# Parametrized fixture
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param
```

---

**Last Updated**: January 2026
