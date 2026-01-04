# Petstore API Documentation

Complete API documentation with examples using curl, HTTPie, and Postman.

## Base URL
```
http://localhost:8000
```

## Authentication

### JWT Authentication
The API uses JWT (JSON Web Tokens) for authentication.

**Token Lifetime:**
- Access Token: 1 hour
- Refresh Token: 7 days

### Obtain Tokens

**Endpoint:** `POST /v2/user/login/`

**curl:**
```bash
curl -X POST http://localhost:8000/v2/user/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

**HTTPie:**
```bash
http POST http://localhost:8000/v2/user/login/ \
  username=testuser password=testpass123
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "phone": null,
    "user_status": 0
  },
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Refresh Access Token

**Endpoint:** `POST /api/token/refresh/`

**curl:**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"your_refresh_token_here"}'
```

**HTTPie:**
```bash
http POST http://localhost:8000/api/token/refresh/ \
  refresh=your_refresh_token_here
```

### Using Tokens in Requests

Include the access token in the Authorization header:

**curl:**
```bash
curl -H "Authorization: Bearer your_access_token" \
  http://localhost:8000/v2/pet/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/pet/ \
  "Authorization: Bearer your_access_token"
```

---

## User Endpoints

### 1. Create User (Register)

**Endpoint:** `POST /v2/user/`

**Authentication:** Not required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/user/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "1234567890",
    "user_status": 1
  }'
```

**HTTPie:**
```bash
http POST http://localhost:8000/v2/user/ \
  username=newuser \
  email=user@example.com \
  password=securepass123 \
  first_name=John \
  last_name=Doe \
  phone=1234567890 \
  user_status=1
```

### 2. Get All Users

**Endpoint:** `GET /v2/user/`

**Authentication:** Required

**curl:**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/user/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/user/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 3. Get User by Username

**Endpoint:** `GET /v2/user/{username}/`

**Authentication:** Required

**curl:**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/user/testuser/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/user/testuser/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 4. Update User

**Endpoint:** `PUT /v2/user/{username}/` or `PATCH /v2/user/{username}/`

**Authentication:** Required (own profile or admin)

**curl:**
```bash
curl -X PATCH http://localhost:8000/v2/user/testuser/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","phone":"9876543210"}'
```

**HTTPie:**
```bash
http PATCH http://localhost:8000/v2/user/testuser/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  first_name=Jane \
  phone=9876543210
```

### 5. Delete User

**Endpoint:** `DELETE /v2/user/{username}/`

**Authentication:** Required (own profile or admin)

**curl:**
```bash
curl -X DELETE http://localhost:8000/v2/user/testuser/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**HTTPie:**
```bash
http DELETE http://localhost:8000/v2/user/testuser/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 6. Get Current User Profile

**Endpoint:** `GET /v2/user/me/`

**Authentication:** Required

**Description:** Get the profile information of the currently authenticated user.

**curl:**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/user/me/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/user/me/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "phone": "1234567890",
  "user_status": 1
}
```

**Status Codes:**
- `200 OK`: Successfully retrieved user profile
- `401 Unauthorized`: Not authenticated (missing or invalid token)

**Notes:**
- This endpoint always returns the profile of the authenticated user
- Password is never included in the response
- Useful for profile pages, user menus, and session validation

### 7. Logout

**Endpoint:** `POST /v2/user/logout/`

**Authentication:** Required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/user/logout/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"refresh":"your_refresh_token"}'
```

**HTTPie:**
```bash
http POST http://localhost:8000/v2/user/logout/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  refresh=your_refresh_token
```

### 8. Create Multiple Users

**Endpoint:** `POST /v2/user/createWithList/`

**Authentication:** Not required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/user/createWithList/ \
  -H "Content-Type: application/json" \
  -d '[
    {"username":"user1","email":"user1@example.com","password":"pass123"},
    {"username":"user2","email":"user2@example.com","password":"pass456"}
  ]'
```

---

## Pet Endpoints

### 1. Create a Pet

**Endpoint:** `POST /v2/pet/`

**Authentication:** Required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/pet/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fluffy",
    "status": "available",
    "photo_urls": ["http://example.com/fluffy.jpg"],
    "category_id": 1,
    "tag_ids": [1, 2]
  }'
```

**HTTPie:**
```bash
http POST http://localhost:8000/v2/pet/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  name=Fluffy \
  status=available \
  photo_urls:='["http://example.com/fluffy.jpg"]' \
  category_id=1 \
  tag_ids:='[1,2]'
```

### 2. Get All Pets

**Endpoint:** `GET /v2/pet/`

**Authentication:** Not required

**curl:**
```bash
curl http://localhost:8000/v2/pet/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/pet/
```

### 3. Get Pet by ID

**Endpoint:** `GET /v2/pet/{id}/`

**Authentication:** Not required

**curl:**
```bash
curl http://localhost:8000/v2/pet/1/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/pet/1/
```

### 4. Find Pets by Status

**Endpoint:** `GET /v2/pet/findByStatus/?status={status}`

**Authentication:** Not required

**curl:**
```bash
# Single status
curl "http://localhost:8000/v2/pet/findByStatus/?status=available"

# Multiple statuses
curl "http://localhost:8000/v2/pet/findByStatus/?status=available,pending"
```

**HTTPie:**
```bash
http "http://localhost:8000/v2/pet/findByStatus/?status=available"
```

**Valid statuses:** `available`, `pending`, `sold`

### 5. Find Pets by Tags

**Endpoint:** `GET /v2/pet/findByTags/?tags={tags}`

**Authentication:** Not required

**curl:**
```bash
curl "http://localhost:8000/v2/pet/findByTags/?tags=cute,friendly"
```

**HTTPie:**
```bash
http "http://localhost:8000/v2/pet/findByTags/?tags=cute,friendly"
```

### 6. Update a Pet

**Endpoint:** `PUT /v2/pet/{id}/` or `PATCH /v2/pet/{id}/`

**Authentication:** Required

**curl:**
```bash
curl -X PATCH http://localhost:8000/v2/pet/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fluffy Updated","status":"sold"}'
```

**HTTPie:**
```bash
http PATCH http://localhost:8000/v2/pet/1/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  name="Fluffy Updated" \
  status=sold
```

### 7. Delete a Pet

**Endpoint:** `DELETE /v2/pet/{id}/`

**Authentication:** Required

**curl:**
```bash
curl -X DELETE http://localhost:8000/v2/pet/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**HTTPie:**
```bash
http DELETE http://localhost:8000/v2/pet/1/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 8. Upload Pet Image

**Endpoint:** `POST /v2/pet/{id}/uploadImage/`

**Authentication:** Required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/pet/1/uploadImage/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "additionalMetadata=Pet photo"
```

**HTTPie:**
```bash
http --form POST http://localhost:8000/v2/pet/1/uploadImage/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  file@/path/to/image.jpg \
  additionalMetadata="Pet photo"
```

---

## Store Endpoints

### 1. Get Inventory

**Endpoint:** `GET /v2/store/orders/inventory/`

**Authentication:** Not required

**curl:**
```bash
curl http://localhost:8000/v2/store/orders/inventory/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/store/orders/inventory/
```

**Response:**
```json
{
  "available": 10,
  "pending": 5,
  "sold": 3
}
```

### 2. Place an Order

**Endpoint:** `POST /v2/store/orders/`

**Authentication:** Required

**curl:**
```bash
curl -X POST http://localhost:8000/v2/store/orders/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "quantity": 2,
    "status": "placed",
    "ship_date": "2026-01-15T10:00:00Z"
  }'
```

**HTTPie:**
```bash
http POST http://localhost:8000/v2/store/orders/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  pet_id=1 \
  quantity=2 \
  status=placed \
  ship_date="2026-01-15T10:00:00Z"
```

### 3. Get All Orders

**Endpoint:** `GET /v2/store/orders/`

**Authentication:** Required

**curl:**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/store/orders/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/store/orders/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 4. Get Order by ID

**Endpoint:** `GET /v2/store/orders/{id}/`

**Authentication:** Required

**curl:**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/v2/store/orders/1/
```

**HTTPie:**
```bash
http http://localhost:8000/v2/store/orders/1/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

### 5. Update an Order

**Endpoint:** `PUT /v2/store/orders/{id}/` or `PATCH /v2/store/orders/{id}/`

**Authentication:** Required

**curl:**
```bash
curl -X PATCH http://localhost:8000/v2/store/orders/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"approved","complete":true}'
```

**HTTPie:**
```bash
http PATCH http://localhost:8000/v2/store/orders/1/ \
  "Authorization: Bearer $ACCESS_TOKEN" \
  status=approved \
  complete:=true
```

### 6. Delete an Order

**Endpoint:** `DELETE /v2/store/orders/{id}/`

**Authentication:** Required

**Note:** Cannot delete completed orders

**curl:**
```bash
curl -X DELETE http://localhost:8000/v2/store/orders/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**HTTPie:**
```bash
http DELETE http://localhost:8000/v2/store/orders/1/ \
  "Authorization: Bearer $ACCESS_TOKEN"
```

---

## Category & Tag Endpoints

### Create Category

**Endpoint:** `POST /v2/pet/categories/`

**curl:**
```bash
curl -X POST http://localhost:8000/v2/pet/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Dogs"}'
```

### Create Tag

**Endpoint:** `POST /v2/pet/tags/`

**curl:**
```bash
curl -X POST http://localhost:8000/v2/pet/tags/ \
  -H "Content-Type: application/json" \
  -d '{"name":"friendly"}'
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input data",
  "details": {}
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You can only update your own profile"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```
