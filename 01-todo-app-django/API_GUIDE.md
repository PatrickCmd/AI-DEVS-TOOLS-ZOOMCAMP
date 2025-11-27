# REST API Documentation

## Overview

The Django TODO application provides a comprehensive RESTful API built with Django REST Framework (DRF) for managing TODO items programmatically. The API follows REST principles and includes full CRUD operations, filtering, searching, and custom actions.

## Features

- Full CRUD operations for TODO items
- Pagination support (10 items per page)
- Filtering by resolved status
- Full-text search across title and description
- Sorting by multiple fields
- Custom actions (toggle resolved, list resolved/unresolved/overdue)
- OpenAPI/Swagger documentation
- JSON responses
- Comprehensive error handling

## Base URL

```
http://localhost:8000/api/
```

## Documentation URLs

### Interactive API Documentation

- **Swagger UI:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
  - Interactive API explorer with "Try it out" functionality
  - Test endpoints directly from your browser
  - View request/response schemas

- **ReDoc:** [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
  - Alternative documentation view
  - Clean, responsive design
  - Better for reading and reference

- **OpenAPI Schema:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
  - Raw OpenAPI 3.0 schema in YAML format
  - Use with tools like Postman, Insomnia, or code generators

## Endpoints

### List TODOs

```http
GET /api/todos/
```

Returns a paginated list of all TODO items.

**Query Parameters:**
- `is_resolved` (boolean): Filter by resolved status (`true` or `false`)
- `search` (string): Search in title and description
- `ordering` (string): Order by field (prefix with `-` for descending)
  - Available fields: `created_at`, `due_date`, `title`, `is_resolved`
- `page` (integer): Page number for pagination

**Example Requests:**

```bash
# Get all TODOs
curl http://localhost:8000/api/todos/

# Get resolved TODOs
curl http://localhost:8000/api/todos/?is_resolved=true

# Search for TODOs
curl http://localhost:8000/api/todos/?search=meeting

# Order by due date (ascending)
curl http://localhost:8000/api/todos/?ordering=due_date

# Order by created date (descending)
curl http://localhost:8000/api/todos/?ordering=-created_at

# Combine filters
curl "http://localhost:8000/api/todos/?is_resolved=false&ordering=due_date"
```

**Response:**

```json
{
  "count": 10,
  "next": "http://localhost:8000/api/todos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Complete project",
      "due_date": "2025-12-01T10:00:00Z",
      "is_resolved": false,
      "created_at": "2025-11-27T10:00:00Z"
    }
  ]
}
```

### Retrieve a TODO

```http
GET /api/todos/{id}/
```

Get detailed information about a specific TODO item.

**Example Request:**

```bash
curl http://localhost:8000/api/todos/1/
```

**Response:**

```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Django TODO app with REST API",
  "due_date": "2025-12-01T10:00:00Z",
  "is_resolved": false,
  "created_at": "2025-11-27T10:00:00Z",
  "updated_at": "2025-11-27T10:00:00Z"
}
```

### Create a TODO

```http
POST /api/todos/
Content-Type: application/json
```

Create a new TODO item.

**Request Body:**

```json
{
  "title": "New TODO",
  "description": "Optional description with **markdown** support",
  "due_date": "2025-12-01T10:00:00Z"
}
```

**Required Fields:**
- `title` (string, max 200 chars): The TODO title

**Optional Fields:**
- `description` (string): Detailed description (supports markdown)
- `due_date` (datetime): Due date in ISO 8601 format
- `is_resolved` (boolean): Resolved status (defaults to `false`)

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team meeting",
    "description": "Discuss Q4 goals and milestones",
    "due_date": "2025-12-01T14:00:00Z"
  }'
```

**Response (201 Created):**

```json
{
  "id": 2,
  "title": "Team meeting",
  "description": "Discuss Q4 goals and milestones",
  "due_date": "2025-12-01T14:00:00Z",
  "is_resolved": false,
  "created_at": "2025-11-27T10:30:00Z",
  "updated_at": "2025-11-27T10:30:00Z"
}
```

### Update a TODO (Full)

```http
PUT /api/todos/{id}/
Content-Type: application/json
```

Replace all fields of an existing TODO. All fields must be provided.

**Example Request:**

```bash
curl -X PUT http://localhost:8000/api/todos/2/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team meeting (Updated)",
    "description": "Discuss Q4 goals, milestones, and budget",
    "due_date": "2025-12-01T15:00:00Z",
    "is_resolved": false
  }'
```

### Update a TODO (Partial)

```http
PATCH /api/todos/{id}/
Content-Type: application/json
```

Update one or more fields of an existing TODO.

**Example Request:**

```bash
curl -X PATCH http://localhost:8000/api/todos/2/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title only"}'
```

### Delete a TODO

```http
DELETE /api/todos/{id}/
```

Permanently delete a TODO item.

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/api/todos/2/
```

**Response:** 204 No Content

### Toggle Resolved Status

```http
POST /api/todos/{id}/toggle_resolved/
```

Toggle the `is_resolved` status between `true` and `false`.

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/todos/1/toggle_resolved/
```

**Response:**

```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Django TODO app",
  "due_date": "2025-12-01T10:00:00Z",
  "is_resolved": true,
  "created_at": "2025-11-27T10:00:00Z",
  "updated_at": "2025-11-27T11:00:00Z"
}
```

### List Resolved TODOs

```http
GET /api/todos/resolved/
```

Get a paginated list of all resolved TODO items.

**Example Request:**

```bash
curl http://localhost:8000/api/todos/resolved/
```

### List Unresolved TODOs

```http
GET /api/todos/unresolved/
```

Get a paginated list of all unresolved TODO items.

**Example Request:**

```bash
curl http://localhost:8000/api/todos/unresolved/
```

### List Overdue TODOs

```http
GET /api/todos/overdue/
```

Get a paginated list of all unresolved TODO items with due dates in the past.

**Example Request:**

```bash
curl http://localhost:8000/api/todos/overdue/
```

## Response Formats

### Success Responses

- **200 OK**: Request successful, data returned
- **201 Created**: Resource created successfully
- **204 No Content**: Request successful, no data to return (e.g., DELETE)

### Error Responses

- **400 Bad Request**: Validation error or invalid request data
- **404 Not Found**: Resource not found

**Example Error Response:**

```json
{
  "title": [
    "This field is required."
  ]
}
```

## Pagination

All list endpoints are paginated with 10 items per page by default.

**Pagination Response Structure:**

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/todos/?page=2",
  "previous": null,
  "results": [...]
}
```

**Fields:**
- `count`: Total number of items
- `next`: URL for the next page (null if last page)
- `previous`: URL for the previous page (null if first page)
- `results`: Array of TODO items for current page

## Data Types

### TODO Object

```typescript
{
  id: number;              // Auto-generated, read-only
  title: string;           // Required, max 200 characters
  description: string;     // Optional, supports markdown
  due_date: string | null; // Optional, ISO 8601 datetime
  is_resolved: boolean;    // Default: false
  created_at: string;      // Auto-generated, read-only
  updated_at: string;      // Auto-generated, read-only
}
```

### TODO List Object

Lightweight version used in list views:

```typescript
{
  id: number;              // Auto-generated, read-only
  title: string;
  due_date: string | null;
  is_resolved: boolean;
  created_at: string;      // Auto-generated, read-only
}
```

## Date Format

All dates use ISO 8601 format with timezone:

```
YYYY-MM-DDTHH:MM:SSZ
```

**Examples:**
- `2025-12-01T10:00:00Z` (UTC)
- `2025-12-01T14:30:00+00:00` (UTC with offset)

## Examples with Python

### Using `requests` library

```python
import requests

BASE_URL = "http://localhost:8000/api"

# List all TODOs
response = requests.get(f"{BASE_URL}/todos/")
todos = response.json()

# Create a TODO
new_todo = {
    "title": "Buy groceries",
    "description": "- Milk\n- Bread\n- Eggs",
    "due_date": "2025-12-01T10:00:00Z"
}
response = requests.post(f"{BASE_URL}/todos/", json=new_todo)
created = response.json()

# Update a TODO
response = requests.patch(
    f"{BASE_URL}/todos/{created['id']}/",
    json={"is_resolved": True}
)

# Delete a TODO
response = requests.delete(f"{BASE_URL}/todos/{created['id']}/")
```

## Examples with JavaScript

### Using `fetch` API

```javascript
const BASE_URL = 'http://localhost:8000/api';

// List all TODOs
fetch(`${BASE_URL}/todos/`)
  .then(res => res.json())
  .then(data => console.log(data));

// Create a TODO
fetch(`${BASE_URL}/todos/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Buy groceries',
    description: '- Milk\n- Bread\n- Eggs',
    due_date: '2025-12-01T10:00:00Z'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));

// Toggle resolved status
fetch(`${BASE_URL}/todos/1/toggle_resolved/`, {
  method: 'POST'
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Examples with cURL

### Complete CRUD workflow

```bash
# 1. Create a TODO
curl -X POST http://localhost:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive API guide with examples"
  }'
# Returns: {"id": 5, "title": "Complete API documentation", ...}

# 2. List all TODOs
curl http://localhost:8000/api/todos/

# 3. Get specific TODO
curl http://localhost:8000/api/todos/5/

# 4. Update TODO
curl -X PATCH http://localhost:8000/api/todos/5/ \
  -H "Content-Type: application/json" \
  -d '{"is_resolved": true}'

# 5. Delete TODO
curl -X DELETE http://localhost:8000/api/todos/5/
```

## Testing the API

### Using the Makefile

```bash
# Run all API tests
make test-api

# Run all tests with coverage
make test

# Run specific test class
docker compose run --rm web uv run pytest todo/tests/test_api.py::TestTodoListAPI -v
```

### Manual Testing with HTTPie

Install [HTTPie](https://httpie.io/):

```bash
pip install httpie
```

Example requests:

```bash
# List TODOs
http GET localhost:8000/api/todos/

# Create TODO
http POST localhost:8000/api/todos/ \
  title="Test TODO" \
  description="Testing with HTTPie"

# Update TODO
http PATCH localhost:8000/api/todos/1/ \
  title="Updated title"

# Toggle resolved
http POST localhost:8000/api/todos/1/toggle_resolved/

# Delete TODO
http DELETE localhost:8000/api/todos/1/
```

## Rate Limiting

Currently, the API does not implement rate limiting. For production use, consider enabling DRF's throttling:

```python
# In settings.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
    },
}
```

## Authentication

Currently, the API uses `AllowAny` permission, meaning no authentication is required. For production use, consider implementing authentication:

- Session Authentication (for web clients)
- Token Authentication (for mobile/desktop apps)
- JWT Authentication (for stateless APIs)

## CORS

If you need to access the API from a different domain (e.g., frontend on different port), install `django-cors-headers`:

```bash
uv add django-cors-headers
```

Configure in settings.py:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Your frontend URL
]
```

## Troubleshooting

### API returns 404

- Ensure the server is running: `make up`
- Check the URL starts with `/api/`
- Verify the TODO ID exists

### Validation errors

- Check required fields are provided
- Ensure data types match (string, boolean, datetime)
- Verify datetime format is ISO 8601

### Schema not loading

- Run migrations: `make migrate`
- Restart server: `make restart`
- Check browser console for JavaScript errors

## Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Best Practices](https://restfulapi.net/)

## Support

For issues with the API:
1. Check this guide
2. Review the interactive Swagger documentation at `/api/docs/`
3. Run the test suite: `make test-api`
4. Check Django logs: `make logs`
