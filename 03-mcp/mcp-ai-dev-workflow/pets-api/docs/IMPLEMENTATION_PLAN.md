# Pets Store API Implementation Plan

## Project Overview
Build a comprehensive Pets Store API using Django REST Framework based on the OpenAPI 3.1.0 specification (Swagger Petstore). The API will include pet management, store orders, user management with authentication, and a containerized environment.

## Technology Stack

### Core Technologies
- **Backend Framework**: Django 5.x with Django REST Framework (DRF)
- **Data Validation**: Pydantic v2 for request/response validation
- **Database**: PostgreSQL 15+
- **Authentication**: Django REST Framework Token Authentication + OAuth2 support
- **Dependency Management**: uv (modern Python package installer)
- **Testing**: pytest with pytest-django
- **Containerization**: Docker & Docker Compose

### Key Libraries
- `django` (5.2+) - Web framework
- `djangorestframework` - REST API toolkit
- `pydantic` (v2) - Data validation
- `pydantic-settings` - Settings management
- `psycopg2-binary` - PostgreSQL adapter
- `pytest` - Testing framework
- `pytest-django` - Django plugin for pytest
- `pytest-cov` - Coverage reporting
- `factory-boy` - Test fixtures
- `drf-spectacular` - OpenAPI schema generation

## Project Structure

```
03-mcp/mcp-ai-dev-workflow/pets-api/
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   └── API_DOCUMENTATION.md
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── pets/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── filters.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       ├── test_serializers.py
│   │   │       └── factories.py
│   │   ├── store/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── factories.py
│   │   └── users/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── permissions.py
│   │       └── tests/
│   │           ├── __init__.py
│   │           ├── test_models.py
│   │           ├── test_views.py
│   │           └── factories.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── pydantic_models.py
│   │   ├── validators.py
│   │   └── exceptions.py
│   └── manage.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── integration/
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.override.yml
├── pyproject.toml
├── pytest.ini
├── README.md
└── openai.yml
```

## Implementation Phases

### Phase 1: Project Setup and Infrastructure
**Estimated Complexity**: Low-Medium

#### 1.1 Initialize Project with uv
- Set up uv for dependency management
- Create `pyproject.toml` with all dependencies
- Configure Python 3.11+ environment

#### 1.2 Django Project Initialization
- Create Django project structure
- Set up settings module with environment-based configuration
- Configure Pydantic Settings for environment variables
- Create base settings, development, production, and test settings

#### 1.3 Docker Setup
- Create Dockerfile for Django application
- Create docker-compose.yml with:
  - PostgreSQL service (with persistent volume)
  - Django backend service
  - Nginx service (for production-ready setup)
- Configure environment variables
- Set up health checks

#### 1.4 Database Configuration
- Configure PostgreSQL connection
- Set up database migrations structure
- Create initial migration files

### Phase 2: Data Models and Pydantic Integration
**Estimated Complexity**: Medium

#### 2.1 Pydantic Models (common/pydantic_models.py)
Based on OpenAPI spec components/schemas:

- `CategoryModel` - Pet category
- `TagModel` - Pet tags
- `PetModel` - Pet entity with validation
- `OrderModel` - Store order
- `UserModel` - User entity
- `ApiResponseModel` - API response wrapper

#### 2.2 Django Models

**Pets App** (`apps/pets/models.py`):
- `Category` - Pet categories (id, name)
- `Tag` - Pet tags (id, name)
- `Pet` - Main pet model:
  - id (auto-generated)
  - name (required)
  - category (ForeignKey to Category)
  - photo_urls (JSONField/ArrayField)
  - tags (ManyToMany to Tag)
  - status (choices: available, pending, sold)
  - created_at, updated_at

**Store App** (`apps/store/models.py`):
- `Order` - Store orders:
  - id (auto-generated)
  - pet (ForeignKey to Pet)
  - user (ForeignKey to User)
  - quantity
  - ship_date
  - status (choices: placed, approved, delivered)
  - complete (boolean)
  - created_at, updated_at

**Users App** (`apps/users/models.py`):
- `User` - Extended Django User:
  - username (unique)
  - first_name
  - last_name
  - email
  - password (hashed)
  - phone
  - user_status (integer status code)
  - is_active, is_staff, date_joined

#### 2.3 Model Validators
- Integrate Pydantic validators with Django models
- Create custom field validators
- Add model-level validation

### Phase 3: Authentication and Authorization
**Estimated Complexity**: Medium

#### 3.1 User Authentication
- Implement Token Authentication
- Configure OAuth2 support (for petstore_auth)
- Set up API Key authentication
- Create authentication backends

#### 3.2 Permissions
**Pets Permissions**:
- `write:pets` - Can modify pets
- `read:pets` - Can read pets

**Custom Permission Classes**:
- `HasPetPermission` - Check OAuth2 scopes
- `IsOwnerOrReadOnly` - User can only modify their own resources
- `ApiKeyPermission` - API key authentication

#### 3.3 User Management Endpoints
Based on OpenAPI spec:
- `POST /user` - Create user
- `POST /user/createWithArray` - Create users with array
- `POST /user/createWithList` - Create users with list
- `GET /user/login` - Login user (return token)
- `GET /user/logout` - Logout user
- `GET /user/{username}` - Get user by username
- `PUT /user/{username}` - Update user
- `DELETE /user/{username}` - Delete user

### Phase 4: Pet Management API
**Estimated Complexity**: High

#### 4.1 Pet Serializers (`apps/pets/serializers.py`)
- `CategorySerializer`
- `TagSerializer`
- `PetSerializer` - With nested serializers
- `PetCreateSerializer` - For POST requests
- `PetUpdateSerializer` - For PUT requests
- `PetListSerializer` - For list views

#### 4.2 Pet Views (`apps/pets/views.py`)
Using DRF ViewSets and APIViews:

- `PetViewSet`:
  - `POST /pet` - Add new pet (requires: write:pets, read:pets)
  - `PUT /pet` - Update existing pet (requires: write:pets, read:pets)
  - `GET /pet/{petId}` - Get pet by ID (requires: api_key)
  - `POST /pet/{petId}` - Update pet with form data (requires: write:pets, read:pets)
  - `DELETE /pet/{petId}` - Delete pet (requires: write:pets, read:pets)
  - `POST /pet/{petId}/uploadImage` - Upload pet image (requires: write:pets, read:pets)

- `PetFilterViewSet`:
  - `GET /pet/findByStatus` - Filter pets by status (requires: write:pets, read:pets)
  - `GET /pet/findByTags` - Filter pets by tags [DEPRECATED] (requires: write:pets, read:pets)

#### 4.3 Pet Filters and Search
- Implement django-filter for status filtering
- Implement tag-based filtering
- Add pagination support

#### 4.4 Image Upload Handling
- Configure media files handling
- Implement image upload for pets
- Add image validation (size, format)

### Phase 5: Store Management API
**Estimated Complexity**: Medium

#### 5.1 Store Serializers (`apps/store/serializers.py`)
- `OrderSerializer` - Full order details
- `OrderCreateSerializer` - For POST requests
- `InventorySerializer` - For inventory response

#### 5.2 Store Views (`apps/store/views.py`)
- `StoreInventoryView`:
  - `GET /store/inventory` - Get inventory by status (requires: api_key)

- `OrderViewSet`:
  - `POST /store/order` - Place order
  - `GET /store/order/{orderId}` - Get order by ID
  - `DELETE /store/order/{orderId}` - Delete order

#### 5.3 Inventory Management
- Implement inventory calculation logic
- Create aggregation queries for pet status counts

### Phase 6: Testing Strategy
**Estimated Complexity**: High

#### 6.1 Test Infrastructure
- Configure pytest with pytest.ini
- Set up conftest.py with fixtures
- Configure test database
- Set up factory_boy factories

#### 6.2 Unit Tests

**Pet App Tests**:
- `test_models.py`:
  - Test Pet model creation
  - Test Category and Tag relationships
  - Test status transitions
  - Test model validation

- `test_serializers.py`:
  - Test PetSerializer validation
  - Test nested serializer behavior
  - Test read-only fields

- `test_views.py`:
  - Test CRUD operations
  - Test filtering by status
  - Test filtering by tags
  - Test image upload
  - Test authentication and permissions

**Store App Tests**:
- `test_models.py`:
  - Test Order model creation
  - Test order status transitions
  - Test relationships with Pet and User

- `test_views.py`:
  - Test order placement
  - Test inventory retrieval
  - Test order CRUD operations

**User App Tests**:
- `test_models.py`:
  - Test extended User model
  - Test user creation and validation

- `test_views.py`:
  - Test user registration
  - Test login/logout
  - Test user CRUD operations
  - Test permissions

#### 6.3 Integration Tests
- Test complete workflows (e.g., create pet → place order)
- Test authentication flows
- Test error handling and edge cases

#### 6.4 Test Coverage
- Aim for 90%+ code coverage
- Configure pytest-cov
- Generate coverage reports

### Phase 7: API Documentation and Validation
**Estimated Complexity**: Low-Medium

#### 7.1 OpenAPI Schema
- Use drf-spectacular to generate OpenAPI schema
- Validate against provided openai.yml
- Ensure all endpoints match specification

#### 7.2 API Documentation
- Configure Swagger UI
- Configure ReDoc
- Add API examples and descriptions

#### 7.3 Request/Response Validation
- Ensure Pydantic models validate all requests
- Add custom exception handlers
- Implement proper error responses

### Phase 8: Production Readiness
**Estimated Complexity**: Medium

#### 8.1 Security
- Configure CORS
- Set up rate limiting
- Add security headers
- Configure secure cookie settings
- Add SQL injection protection (Django ORM handles this)
- Add XSS protection

#### 8.2 Performance
- Add database indexes
- Configure connection pooling
- Set up query optimization
- Add caching (Redis optional)

#### 8.3 Logging and Monitoring
- Configure structured logging
- Add request/response logging
- Set up error tracking
- Add health check endpoints

#### 8.4 Deployment Configuration
- Production-ready Dockerfile
- Multi-stage Docker builds
- Nginx reverse proxy configuration
- Static files handling
- Database backup strategy

## Development Workflow

### 1. Environment Setup
```bash
# Clone/navigate to project
cd 03-mcp/mcp-ai-dev-workflow/pets-api

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 2. Docker Development
```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Run tests
docker-compose exec backend pytest

# View logs
docker-compose logs -f backend
```

### 3. Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest src/apps/pets/tests/test_views.py

# Run with verbose output
pytest -v
```

### 4. Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## API Endpoints Summary

### Pet Endpoints
- `POST /pet` - Add new pet
- `PUT /pet` - Update existing pet
- `GET /pet/findByStatus` - Find pets by status
- `GET /pet/findByTags` - Find pets by tags (deprecated)
- `GET /pet/{petId}` - Get pet by ID
- `POST /pet/{petId}` - Update pet with form data
- `DELETE /pet/{petId}` - Delete pet
- `POST /pet/{petId}/uploadImage` - Upload image

### Store Endpoints
- `GET /store/inventory` - Get inventory
- `POST /store/order` - Place order
- `GET /store/order/{orderId}` - Get order by ID
- `DELETE /store/order/{orderId}` - Delete order

### User Endpoints
- `POST /user` - Create user
- `POST /user/createWithArray` - Create users with array
- `POST /user/createWithList` - Create users with list
- `GET /user/login` - Login
- `GET /user/logout` - Logout
- `GET /user/{username}` - Get user
- `PUT /user/{username}` - Update user
- `DELETE /user/{username}` - Delete user

## Security Schemes
1. **petstore_auth** (OAuth2):
   - Authorization URL: `http://petstore.swagger.io/oauth/dialog`
   - Scopes: `write:pets`, `read:pets`

2. **api_key**:
   - Type: API Key
   - Location: Header
   - Name: `api_key`

## Key Design Decisions

### 1. Pydantic Integration
- Use Pydantic for request/response validation
- Keep Django models for ORM and database
- Bridge between Pydantic and Django serializers

### 2. Authentication Strategy
- Primary: Token-based authentication
- Secondary: OAuth2 for specific endpoints
- API Key for read-only operations

### 3. Image Storage
- Local storage for development
- Prepared for S3/cloud storage in production

### 4. Testing Philosophy
- Unit tests for business logic
- Integration tests for workflows
- Factory Boy for test data generation
- High coverage target (90%+)

### 5. Docker Strategy
- Separate Dockerfile for dev and prod
- docker-compose for local development
- Kubernetes-ready for production scaling

## Dependencies Management (pyproject.toml)

### Production Dependencies
- django >= 5.2
- djangorestframework >= 3.15
- pydantic >= 2.0
- pydantic-settings >= 2.0
- psycopg2-binary >= 2.9
- django-filter >= 24.0
- drf-spectacular >= 0.27
- pillow >= 10.0 (for image handling)
- python-multipart (for file uploads)

### Development Dependencies
- pytest >= 8.0
- pytest-django >= 4.7
- pytest-cov >= 4.1
- factory-boy >= 3.3
- faker >= 22.0
- black (code formatting)
- ruff (linting)
- mypy (type checking)

## Success Criteria

1. All API endpoints from OpenAPI spec are implemented
2. User authentication and authorization working
3. All CRUD operations for pets, orders, and users functional
4. 90%+ test coverage
5. All tests passing
6. Docker environment running smoothly
7. API documentation auto-generated and accurate
8. Pydantic validation on all endpoints
9. Database properly normalized and optimized
10. Production-ready security configurations

## Next Steps

After plan approval, we will proceed with:
1. Phase 1: Project setup with uv and Docker
2. Phase 2: Data models implementation
3. Phase 3: Authentication setup
4. Phases 4-5: API endpoints implementation
5. Phase 6: Comprehensive testing
6. Phases 7-8: Documentation and production readiness

## Notes

- All implementations will follow Django and DRF best practices
- Code will be type-hinted for better IDE support
- Each feature will be tested before moving to the next
- Git commits will be made incrementally
- Environment variables will be used for all sensitive configuration
- The API will be RESTful and follow OpenAPI 3.1.0 specification exactly
