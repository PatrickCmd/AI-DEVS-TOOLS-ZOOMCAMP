# Petstore API

A comprehensive Pets Store API implementation using Django REST Framework, based on the OpenAPI 3.1.0 specification (Swagger Petstore).

## Features

- RESTful API for pet management, store orders, and user management
- **JWT Authentication** (Access & Refresh tokens)
- Pydantic v2 for request/response validation
- PostgreSQL 16 database
- Docker containerization
- Comprehensive test coverage with pytest
- OpenAPI/Swagger documentation
- Custom Django Admin interface

## Tech Stack

- **Python**: 3.12+
- **Backend**: Django 5.2, Django REST Framework 3.15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 16
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-django
- **Package Management**: uv
- **Containerization**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- uv (for local development)

### Installation

1. **Clone the repository and navigate to the project directory:**
```bash
cd 03-mcp/mcp-ai-dev-workflow/pets-api
```

2. **(Optional) Configure environment variables:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your configuration (optional for basic setup)
# You can add Context7 API key here for AI assistance
```

3. **Build and start services using Make:**
```bash
make setup
```

This command will:
- Build Docker containers
- Start all services
- Run database migrations
- Seed sample data (categories and tags)

4. **Create a superuser for admin access:**
```bash
make createsuperuser
```

You'll be prompted to enter:
- Username
- Email address
- Password

Example:
```
Username: admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.
```

5. **Access the application:**
- **API Root**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/ (use superuser credentials)

### Alternative Setup (without Make)

If you prefer not to use Make:

```bash
# Build containers
docker compose build

# Start services
docker compose up -d

# Run migrations
docker compose exec backend python src/manage.py migrate

# Create superuser
docker compose exec backend python src/manage.py createsuperuser
```

## Makefile Commands

The project includes a comprehensive Makefile for common operations:

### Docker Commands
```bash
make build              # Build Docker containers
make up                 # Start all services
make down               # Stop all services
make restart            # Restart all services
make logs               # View all container logs
make logs-backend       # View backend logs only
make logs-db            # View database logs only
```

### Django Commands
```bash
make shell              # Open Django shell
make bash               # Open bash shell in backend container
make db-shell           # Open PostgreSQL shell
make migrate            # Run database migrations
make makemigrations     # Create new migrations
make createsuperuser    # Create Django superuser
make collectstatic      # Collect static files
```

### Testing Commands
```bash
make test               # Run all tests
make test-cov           # Run tests with coverage report
make test-models        # Run model tests only
make test-views         # Run view tests only
make test-admin         # Run admin tests only
make test-users         # Run user app tests
make test-pets          # Run pets app tests
make test-store         # Run store app tests
```

### Code Quality
```bash
make lint               # Run ruff linter
make lint-all           # Run all linters (ruff, flake8, pylint)
make format             # Format code (black + isort)
make format-check       # Check code formatting without making changes
make check              # Run type checking (mypy)
make security           # Run security checks (bandit)
make quality            # Run all quality checks
```

For comprehensive code quality documentation, see [docs/CODE_QUALITY.md](docs/CODE_QUALITY.md).

### Development
```bash
make install            # Install dependencies locally
make shell-plus         # Open enhanced Django shell with shell_plus
make show-urls          # Show all URL patterns
make graph-models       # Generate model diagrams (requires graphviz)
make clean              # Clean up containers and volumes
make reset-db           # Reset database (deletes all data)
make seed-data          # Seed database with sample data
```

### Fixture Management
```bash
make dump-fixtures      # Export all data to fixtures
make dump-pets          # Export pets app data to fixtures
make dump-users         # Export users app data to fixtures
make dump-store         # Export store app data to fixtures
make load-fixtures      # Load all fixtures into database
make create-sample      # Create and load sample fixtures for testing
```

## Fixture Management

Fixtures are pre-defined data sets that can be loaded into the database. They're useful for testing, development, and sharing consistent data with contributors.

### Quick Start with Fixtures

```bash
# Create sample categories and tags
make create-sample

# Export your current database to fixtures
make dump-fixtures

# Load fixtures from files
make load-fixtures
```

### Use Cases

1. **Testing**: Load consistent data before running tests
2. **Development**: Start with pre-populated data
3. **Collaboration**: Share data with team members
4. **Backup**: Create snapshots of important data

### Available Fixtures

- **sample_categories_tags.json**: Pre-created categories (Dogs, Cats, Birds, Fish, Reptiles) and tags (friendly, playful, calm, trained, energetic, gentle, social, independent)

For detailed fixture documentation, see [fixtures/README.md](fixtures/README.md).

## Development Tools & AI Assistance

### Context7 MCP Server

This project supports **Context7 MCP (Model Context Protocol)** for accessing up-to-date library documentation during development with AI coding assistants.

**Why use Context7?**
- Get current, version-specific documentation for Django, DRF, and other libraries
- Eliminate outdated code examples and API hallucinations
- Access real code patterns from official sources
- Works seamlessly with Claude Code, VSCode, and Cursor

**Quick Setup:**

```bash
# For Claude Code CLI
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY

# For VSCode - add to settings.json
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"],
        "env": {
          "CONTEXT7_API_KEY": "ctx7sk_your_key"
        }
      }
    }
  }
}
```

**Usage in prompts:**

```
Use context7 to help me implement pagination with Django REST Framework 3.15
```

```
Remember to use context7. Show me how to add GraphQL support with graphene-django
```

For complete installation instructions, configuration options, best practices, and troubleshooting, see the [Context7 MCP Guide](docs/CONTEXT7_MCP_GUIDE.md).

## Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/v2/user/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    ...
  },
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 2. Login (Get Tokens)

```bash
curl -X POST http://localhost:8000/v2/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 3. Use Token in Requests

```bash
# Set token as environment variable
export ACCESS_TOKEN="your_access_token_here"

# Use in requests
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/pet/
```

### 4. Refresh Access Token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"your_refresh_token"}'
```

## API Endpoints

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/v2/user/` | Register new user | No |
| POST | `/v2/user/login/` | Login user | No |
| POST | `/v2/user/logout/` | Logout user | Yes |
| GET | `/v2/user/` | List all users | Yes |
| GET | `/v2/user/{username}/` | Get user by username | Yes |
| PUT/PATCH | `/v2/user/{username}/` | Update user | Yes (own profile) |
| DELETE | `/v2/user/{username}/` | Delete user | Yes (own account) |
| POST | `/v2/user/createWithList/` | Create multiple users | No |

### Pet Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/v2/pet/` | Create new pet | Yes |
| GET | `/v2/pet/` | List all pets | No |
| GET | `/v2/pet/{id}/` | Get pet by ID | No |
| PUT/PATCH | `/v2/pet/{id}/` | Update pet | Yes |
| DELETE | `/v2/pet/{id}/` | Delete pet | Yes |
| GET | `/v2/pet/findByStatus/` | Find pets by status | No |
| GET | `/v2/pet/findByTags/` | Find pets by tags | No |
| POST | `/v2/pet/{id}/uploadImage/` | Upload pet image | Yes |

### Store Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/v2/store/orders/inventory/` | Get inventory | No |
| POST | `/v2/store/orders/` | Create order | Yes |
| GET | `/v2/store/orders/` | List orders | Yes |
| GET | `/v2/store/orders/{id}/` | Get order by ID | Yes |
| PUT/PATCH | `/v2/store/orders/{id}/` | Update order | Yes |
| DELETE | `/v2/store/orders/{id}/` | Delete order | Yes |

### Categories & Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/v2/pet/categories/` | Create category | No |
| GET | `/v2/pet/categories/` | List categories | No |
| POST | `/v2/pet/tags/` | Create tag | No |
| GET | `/v2/pet/tags/` | List tags | No |

For detailed API documentation with curl and HTTPie examples, see [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

## Testing

The project includes comprehensive test coverage with pytest.

### Run All Tests
```bash
make test
```

### Run Tests with Coverage
```bash
make test-cov
```

### Run Specific Test Categories
```bash
# Model tests
make test-models

# View tests
make test-views

# Admin tests
make test-admin

# Specific app tests
make test-users
make test-pets
make test-store
```

### Test Coverage
- **116 unit tests** covering:
  - Model creation and validation
  - API endpoints (CRUD operations)
  - Authentication and authorization
  - Admin configurations
  - Edge cases and error handling
- **79%+ code coverage**

### Testing Documentation

For comprehensive testing documentation, see:
- **[Pytest Guide](docs/PYTEST_GUIDE.md)**: Complete guide to pytest, fixtures, scopes, and Django integration
  - Understanding pytest basics
  - Working with fixtures and scopes
  - Django-specific testing patterns
  - Project-specific fixtures explained
  - Configuration and best practices
  - Troubleshooting common issues

## Admin Interface

Access the custom admin interface at http://localhost:8000/admin/

**Features:**
- Custom branding: "Pets Store Admin"
- Full CRUD operations for all models
- Advanced filtering and search
- Bulk actions
- Inline editing for related models

**First Time Admin Access:**
1. Create a superuser: `make createsuperuser`
2. Navigate to http://localhost:8000/admin/
3. Login with superuser credentials

## Development

### Local Development Setup

1. **Create virtual environment:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
make install
# or
uv pip install -e ".[dev]"
```

3. **Start services:**
```bash
make up
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make check

# Run all quality checks
make quality
```

### Database Management

```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate

# Reset database (WARNING: deletes all data)
make reset-db

# Seed sample data
make seed-data

# Access PostgreSQL shell
make db-shell
```

### Useful Commands

```bash
# View logs
make logs

# Open Django shell
make shell

# Open bash in container
make bash

# Clean up everything
make clean
```

## Project Structure

```
pets-api/
├── src/
│   ├── config/          # Django settings and configuration
│   │   ├── settings/    # Environment-specific settings
│   │   ├── urls.py      # URL configuration
│   │   └── admin.py     # Custom admin configuration
│   ├── pets/            # Pet management app
│   │   ├── models.py    # Category, Tag, Pet models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── tests/       # Unit tests
│   ├── store/           # Store/order management app
│   │   ├── models.py    # Order model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── tests/       # Unit tests
│   ├── users/           # User management app
│   │   ├── models.py    # Custom User model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── tests/       # Unit tests
│   ├── common/          # Shared utilities
│   │   ├── env_settings.py    # Pydantic settings
│   │   └── pydantic_models.py # Pydantic validation models
│   ├── conftest.py      # Pytest fixtures
│   └── manage.py        # Django management script
├── docker/              # Docker configuration
│   └── backend/
│       └── Dockerfile
├── postman/             # Postman collection
│   └── Petstore_API.postman_collection.json
├── docs/                # Documentation
│   ├── API_DOCUMENTATION.md        # API endpoint reference
│   ├── CODE_QUALITY.md            # Linting and code quality guide
│   ├── CONTEXT7_MCP_GUIDE.md      # Context7 MCP setup and usage
│   ├── CONTEXT7_QUICK_REFERENCE.md # Quick reference for Context7
│   ├── DJANGO_LOGGING_GUIDE.md    # Complete Django logging guide
│   ├── PYTEST_GUIDE.md            # Pytest, fixtures, and Django testing
│   └── QUICK_START.md             # 5-minute setup guide
├── docker-compose.yml   # Docker Compose configuration
├── Makefile            # Automation commands
├── pyproject.toml      # Project dependencies
└── pytest.ini          # Pytest configuration
```

## Testing with Postman

A Postman collection is available at `postman/Petstore_API.postman_collection.json`.

### Import Collection
1. Open Postman
2. Click "Import" button
3. Select the collection file
4. Collection includes all endpoints with example requests

### Environment Variables
Set these variables in Postman:
- `base_url`: http://localhost:8000
- `access_token`: (obtained from login)
- `refresh_token`: (obtained from login)

The collection will automatically extract and save tokens from login/register responses.

## Environment Variables

Key environment variables (configured in `.env`):

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend

# Database
DATABASE_URL=postgresql://petstore:petstore@db:5432/petstore_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Troubleshooting

### Container won't start
```bash
# Check logs
make logs

# Rebuild containers
make clean
make build
make up
```

### Database connection errors
```bash
# Ensure database is healthy
docker compose ps

# Reset database
make reset-db
```

### Tests failing
```bash
# Clean up test artifacts
make clean

# Run tests with verbose output
docker compose exec backend pytest src/ -vv
```

### Permission errors
```bash
# Fix permissions on Linux/Mac
sudo chown -R $USER:$USER .
```

### Debugging with shell_plus

For interactive debugging and exploration:

```bash
# Open enhanced Django shell with all models auto-imported
make shell-plus

# Example session:
>>> Pet.objects.filter(status='available').count()
>>> user = User.objects.first()
>>> Order.objects.filter(user=user)
```

### Inspecting URLs and Models

```bash
# See all registered URL patterns
make show-urls

# Generate visual model diagram (requires graphviz)
make graph-models
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Run quality checks: `make quality`
6. Submit a pull request

## License

Apache 2.0 - See LICENSE file for details

## Additional Resources

- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API endpoint reference with curl/HTTPie examples
- [Quick Start Guide](docs/QUICK_START.md) - 5-minute setup guide
- [Code Quality Guide](docs/CODE_QUALITY.md) - Linting, formatting, type checking, and development tools
- [Context7 MCP Guide](docs/CONTEXT7_MCP_GUIDE.md) - Setup and use Context7 for up-to-date library documentation
- [Context7 Quick Reference](docs/CONTEXT7_QUICK_REFERENCE.md) - Quick reference for Context7 usage
- [Fixtures Documentation](fixtures/README.md) - Database fixtures guide
- [Postman Collection](postman/Petstore_API.postman_collection.json) - Import into Postman for easy API testing
- [OpenAPI Specification](openai.yml) - API specification file
