# Quick Start Guide

Get the Petstore API running in under 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Make (optional but recommended)

## 1. Start the Application

### Using Make (Recommended)

```bash
# Navigate to project directory
cd 03-mcp/mcp-ai-dev-workflow/pets-api

# One-command setup
make setup
```

This will:
- Build Docker containers
- Start PostgreSQL and Django services
- Run database migrations
- Seed sample data

### Without Make

```bash
docker compose build
docker compose up -d
docker compose exec backend python src/manage.py migrate
```

## 2. Create Admin User

```bash
# Using Make
make createsuperuser

# Without Make
docker compose exec backend python src/manage.py createsuperuser
```

**Example:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

## 3. Access the Application

- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **API Base URL**: http://localhost:8000/

## 4. Test the API

### Option 1: Using Swagger UI

1. Go to http://localhost:8000/api/docs/
2. Click "Try it out" on any endpoint
3. Execute requests directly from browser

### Option 2: Using curl

**Register a user:**
```bash
curl -X POST http://localhost:8000/v2/user/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login and get tokens:**
```bash
curl -X POST http://localhost:8000/v2/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

**Create a pet (with authentication):**
```bash
# Save the access token from login response
export TOKEN="your_access_token_here"

curl -X POST http://localhost:8000/v2/pet/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fluffy",
    "status": "available",
    "photo_urls": ["http://example.com/fluffy.jpg"]
  }'
```

**Get all pets (no auth required):**
```bash
curl http://localhost:8000/v2/pet/
```

### Option 3: Using Postman

1. Import collection from `postman/Petstore_API.postman_collection.json`
2. Use the "Register User" or "Login" request
3. Token is automatically saved for other requests
4. Execute any endpoint

## 5. Explore the Admin Panel

1. Go to http://localhost:8000/admin/
2. Login with your superuser credentials
3. Manage pets, orders, users, categories, and tags

## Common Commands

```bash
# View logs
make logs

# Run tests
make test

# Stop services
make down

# Restart services
make restart

# View all commands
make help
```

## 6. Working with Fixtures (Optional)

Fixtures are pre-defined datasets useful for testing and development.

### Load Sample Data

```bash
# Create sample categories and tags
make create-sample
```

This will add:
- Categories: Dogs, Cats, Birds, Fish, Reptiles
- Tags: friendly, playful, calm, trained, energetic, gentle, social, independent

### Export Your Data

```bash
# Export all data to fixtures
make dump-fixtures

# Export specific app data
make dump-pets
make dump-users
make dump-store
```

### Load Fixtures

```bash
# Load all fixtures from files
make load-fixtures
```

For more details, see [fixtures/README.md](../fixtures/README.md).

## Next Steps

- Read the [full documentation](../README.md)
- Explore [API endpoints](API_DOCUMENTATION.md)
- Check out the [Postman collection](../postman/)
- Run the test suite: `make test`

## Troubleshooting

### Services won't start
```bash
make logs  # Check what's wrong
make clean # Clean everything
make setup # Start fresh
```

### Can't access admin panel
```bash
# Make sure you created a superuser
make createsuperuser
```

### Database errors
```bash
# Reset the database
make reset-db
```

### Port already in use
Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

## Support

- Check the logs: `make logs`
- Review the [README](../README.md)
- Check the [API Documentation](API_DOCUMENTATION.md)
