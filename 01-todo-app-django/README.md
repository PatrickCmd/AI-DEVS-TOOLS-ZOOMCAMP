# Django TODO Application

A fully functional TODO application built with Django, PostgreSQL, Docker, and comprehensive test coverage using pytest.

## Features

### Web Interface
- Create, edit, and delete TODOs
- Assign due dates to tasks with native date/time picker
- Mark TODOs as resolved/unresolved
- **Markdown support** for rich TODO descriptions (headers, lists, code, tables, etc.)
- Clean and responsive UI with modern CSS
- Admin panel for managing TODOs

### REST API
- Full RESTful API with Django REST Framework
- Complete CRUD operations via HTTP
- Pagination, filtering, and search support
- Custom actions (toggle resolved, list resolved/unresolved/overdue)
- **Interactive Swagger/OpenAPI documentation** at `/api/docs/`
- JSON responses with proper HTTP status codes

### Testing
- Comprehensive test suite with 99% coverage (69 tests)
- 31 API-specific tests covering all endpoints
- Automated testing with pytest

## Technology Stack

- **Backend**: Django 5.2.8
- **Database**: PostgreSQL 15
- **API**: Django REST Framework 3.14
- **API Docs**: drf-spectacular (OpenAPI/Swagger)
- **Container**: Docker & Docker Compose
- **Package Manager**: uv
- **Testing**: pytest with pytest-django
- **Python**: 3.12
- **Markdown**: Python-Markdown 3.10 with extensions

## Project Structure

```
01-todo-app-django/
├── todo_project/          # Django project configuration
│   ├── settings.py        # Project settings
│   └── urls.py            # URL routing
├── todo/                  # TODO app
│   ├── models.py          # Database models (Todo model)
│   ├── views.py           # Class-based views (web UI)
│   ├── forms.py           # TodoForm with date picker
│   ├── urls.py            # Web URL patterns
│   ├── admin.py           # Admin configuration
│   ├── api/               # REST API module
│   │   ├── __init__.py    # API module initialization
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py       # API ViewSets (REST API)
│   │   └── urls.py        # API URL patterns
│   ├── templatetags/      # Custom template filters
│   │   └── markdown_extras.py  # Markdown filter
│   └── tests/             # Test suite (69 tests)
│       ├── test_models.py
│       ├── test_views.py
│       ├── test_urls.py
│       ├── test_templates.py
│       ├── test_markdown.py
│       └── test_api.py    # API tests (31 tests)
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── todo_form.html
│   └── todo_confirm_delete.html
├── static/                # Static files
│   └── css/
│       └── style.css      # Styles + markdown CSS
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Web app container
├── Makefile               # Development automation (40+ commands)
├── pyproject.toml         # Python dependencies
├── pytest.ini             # Pytest configuration
├── .env.example           # Environment variables template
├── .env                   # Environment variables (gitignored)
└── .gitignore             # Git ignore rules
```

## Exercise Answers

### Question 1: Install Django
**Command**: `uv sync --no-build-isolation`

We used `uv` as the package manager to install Django 5.2.8 and all dependencies defined in `pyproject.toml`.

### Question 2: Project and App
**Answer**: `settings.py`

You need to edit `settings.py` to:
- Add the app to `INSTALLED_APPS`
- Configure database settings
- Set up templates directory
- Configure static files

### Question 3: Django Models
**Models Created**: `Todo` model with fields:
- `title` (CharField)
- `description` (TextField)
- `due_date` (DateTimeField)
- `is_resolved` (BooleanField)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

**Next Step**: **Run migrations**
```bash
docker compose run --rm web uv run python manage.py makemigrations
docker compose run --rm web uv run python manage.py migrate
```

### Question 4: TODO Logic
**Answer**: `views.py`

We implemented the TODO logic using class-based views:
- `TodoListView` - Display all TODOs
- `TodoCreateView` - Create new TODO
- `TodoUpdateView` - Edit existing TODO
- `TodoDeleteView` - Delete TODO
- `TodoToggleResolvedView` - Toggle resolved status

### Question 5: Templates
**Answer**: `TEMPLATES['DIRS']` in project's `settings.py`

We registered the templates directory by setting:
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    }
]
```

### Question 6: Tests
**Command**: `pytest` or `python manage.py test`

We implemented comprehensive tests covering:
- Model tests (7 tests)
- View tests (11 tests)
- URL tests (5 tests)
- Template tests (6 tests)
- Markdown tests (9 tests)
- API tests (31 tests)

**Total**: 69 tests with 99% code coverage

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- uv (Python package manager)

### Installation

#### Quick Setup (Recommended - Using Makefile)
```bash
cd 01-todo-app-django

# 1. Copy environment file (optional - has sensible defaults)
cp .env.example .env

# 2. Run complete setup
make setup  # Builds, migrates, creates admin, and starts services
```

That's it! The app is now running at http://localhost:8000

#### Manual Setup (Alternative)
1. Clone the repository and navigate to the project directory:
```bash
cd 01-todo-app-django
```

2. Build and start the services:
```bash
docker compose up -d
```

The application will:
- Pull PostgreSQL image
- Build the Django web container
- Run migrations automatically
- Start the development server

3. Access the application:
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin123`
- **REST API**: http://localhost:8000/api/todos/
- **Swagger Docs**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### Using the Makefile

This project includes a comprehensive Makefile for easy development. See [MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md) for details.

**Common commands:**
```bash
make help          # Show all available commands
make up            # Start services
make down          # Stop services
make test          # Run tests
make test-cov      # Run tests with coverage
make logs          # View logs
make migrate       # Run migrations
make shell         # Open Django shell
```

### Running Tests

#### Using Makefile (Recommended)
```bash
make test          # Run all tests
make test-v        # Run tests with verbose output
make test-cov      # Run tests with coverage report
make test-models   # Run model tests only
make test-views    # Run view tests only
make test-markdown # Run markdown tests only
make test-api      # Run API tests only
```

#### Manual Commands
```bash
docker compose run --rm web uv run pytest -v
docker compose run --rm web uv run pytest --cov=todo --cov-report=html
docker compose run --rm web uv run pytest todo/tests/test_models.py -v
```

### Development Commands

#### Using Makefile (Recommended)
```bash
make makemigrations    # Create migrations
make migrate           # Run migrations
make createsuperuser   # Create superuser
make shell             # Django shell
make logs              # View logs
make down              # Stop services
make clean             # Clean up everything
```

#### Manual Commands
```bash
docker compose run --rm web uv run python manage.py makemigrations
docker compose run --rm web uv run python manage.py migrate
docker compose run --rm web uv run python create_superuser.py
docker compose run --rm web uv run python manage.py shell
docker compose logs -f web
docker compose down
docker compose down -v
```

## Environment Configuration

### Environment Variables

The application uses environment variables for configuration. Copy the example file to get started:

```bash
cp .env.example .env
```

### Available Variables

#### Database Configuration
```bash
POSTGRES_DB=todo_db              # Database name
POSTGRES_USER=todo_user          # Database username
POSTGRES_PASSWORD=todo_password  # Database password (change in production!)
POSTGRES_HOST=db                 # Database host (use 'db' for Docker)
POSTGRES_PORT=5432               # Database port
```

#### Django Configuration
```bash
DJANGO_SECRET_KEY=your-secret-key  # Secret key (MUST change in production!)
DEBUG=True                          # Debug mode (False in production)
```

**Security Notes:**
- ⚠️ **Never commit `.env` to version control** (it's in `.gitignore`)
- ⚠️ **Change `DJANGO_SECRET_KEY` in production**
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- ⚠️ **Use strong passwords in production**
  ```bash
  openssl rand -base64 32
  ```
- ⚠️ **Set `DEBUG=False` in production**

### Default Configuration

The application uses PostgreSQL with these default values:
- Database: `todo_db`
- User: `todo_user`
- Password: `todo_password`
- Host: `db` (Docker service name)
- Port: `5432`

## Markdown Support

The application supports full Markdown formatting in TODO descriptions! You can use:

- **Headers** (`## Heading`)
- **Bold** and *italic* text
- Lists (ordered and unordered)
- `Inline code` and code blocks
- [Links](https://example.com)
- Tables
- Blockquotes
- And more!

See the [Markdown Guide](MARKDOWN_GUIDE.md) for detailed examples and usage.

## REST API

The application provides a complete RESTful API built with Django REST Framework. See [API_GUIDE.md](API_GUIDE.md) for comprehensive documentation.

### Quick API Examples

```bash
# List all TODOs
curl http://localhost:8000/api/todos/

# Create a TODO
curl -X POST http://localhost:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New TODO", "description": "Task description"}'

# Get a specific TODO
curl http://localhost:8000/api/todos/1/

# Update a TODO
curl -X PATCH http://localhost:8000/api/todos/1/ \
  -H "Content-Type: application/json" \
  -d '{"is_resolved": true}'

# Delete a TODO
curl -X DELETE http://localhost:8000/api/todos/1/

# Toggle resolved status
curl -X POST http://localhost:8000/api/todos/1/toggle_resolved/

# List resolved TODOs
curl http://localhost:8000/api/todos/resolved/

# List overdue TODOs
curl http://localhost:8000/api/todos/overdue/
```

### Interactive API Documentation

Visit [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) for interactive Swagger documentation where you can:
- Explore all available endpoints
- Test API calls directly from your browser
- View request/response schemas
- See example payloads

### API Features

- Full CRUD operations (Create, Read, Update, Delete)
- Pagination (10 items per page)
- Filtering by resolved status
- Full-text search across title and description
- Sorting by created_at, due_date, title
- Custom actions (toggle resolved, list resolved/unresolved/overdue)
- OpenAPI/Swagger schema
- Comprehensive validation and error handling

## Test Coverage

The test suite achieves 99% code coverage with 69 tests covering:
- Creating, editing, and deleting TODOs (web and API)
- Marking TODOs as resolved/unresolved
- Model validations and ordering
- View functionality and redirects
- URL routing
- Template rendering
- Markdown rendering and formatting
- Complete API endpoint testing (31 tests)
- Pagination, filtering, and search
- Custom API actions

## Future Enhancements

- User authentication and authorization
- TODO categories/tags
- Priority levels
- Enhanced search and filter functionality
- GraphQL API
- Production deployment configuration
- Real-time updates with WebSockets

## License

This project is developed as part of the AI Dev Tools Zoomcamp course.
