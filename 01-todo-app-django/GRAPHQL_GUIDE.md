# GraphQL API Documentation

## Overview

The Django TODO application provides a complete GraphQL API built with Strawberry GraphQL for managing TODO items programmatically. The API offers an alternative to the REST API with features like flexible queries, type safety, and a single endpoint.

## Features

- **Single Endpoint**: All operations through one URL
- **Type-Safe**: Full type safety with GraphQL schema
- **Flexible Queries**: Request exactly the data you need
- **Pagination**: Built-in pagination for all list queries
- **Filtering & Search**: Filter by status and search across fields
- **Interactive Documentation**: GraphiQL interface with auto-complete
- **Introspection**: Self-documenting API schema

## GraphQL Endpoint

**Base URL:** `http://localhost:8000/graphql/`

**Interactive Documentation:** [http://localhost:8000/graphql/](http://localhost:8000/graphql/)

## Getting Started

### Accessing GraphiQL Interface

1. Start the application:
   ```bash
   make up
   # or: docker compose up -d
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/graphql/
   ```

3. You'll see the GraphiQL interface with:
   - **Query Editor** (left): Write your queries/mutations
   - **Variables Panel** (bottom): Define query variables
   - **Results Panel** (right): View query results
   - **Docs Explorer** (right sidebar): Browse schema documentation

### Making Requests

#### Using GraphiQL (Browser)

Simply type your query in the left panel and click the "Play" button or press `Ctrl+Enter`.

#### Using cURL

```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ todos { items { id title } } }"}'
```

#### Using Python

```python
import requests

url = "http://localhost:8000/graphql/"
query = """
{
  todos {
    items {
      id
      title
      isResolved
    }
  }
}
"""

response = requests.post(url, json={"query": query})
print(response.json())
```

#### Using JavaScript/Fetch

```javascript
fetch('http://localhost:8000/graphql/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      {
        todos {
          items {
            id
            title
            isResolved
          }
        }
      }
    `
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Queries

### List All TODOs

Retrieve a paginated list of all TODO items.

**Query:**
```graphql
{
  todos {
    items {
      id
      title
      description
      dueDate
      isResolved
      createdAt
      updatedAt
    }
    pagination {
      total
      page
      pageSize
      hasNext
      hasPrevious
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "todos": {
      "items": [
        {
          "id": "1",
          "title": "Complete project",
          "description": "Finish the Django TODO app",
          "dueDate": "2025-12-01T10:00:00+00:00",
          "isResolved": false,
          "createdAt": "2025-11-27T10:00:00+00:00",
          "updatedAt": "2025-11-27T10:00:00+00:00"
        }
      ],
      "pagination": {
        "total": 1,
        "page": 1,
        "pageSize": 10,
        "hasNext": false,
        "hasPrevious": false
      }
    }
  }
}
```

**With Pagination:**
```graphql
{
  todos(page: 2, pageSize: 5) {
    items {
      id
      title
    }
    pagination {
      total
      page
      hasNext
      hasPrevious
    }
  }
}
```

**With Filters:**
```graphql
{
  # Only resolved TODOs
  todos(isResolved: true) {
    items {
      id
      title
      isResolved
    }
    pagination {
      total
    }
  }
}
```

**With Search:**
```graphql
{
  # Search in title and description
  todos(search: "meeting") {
    items {
      id
      title
      description
    }
    pagination {
      total
    }
  }
}
```

**With Ordering:**
```graphql
{
  # Order by due date (ascending)
  todos(orderBy: "due_date") {
    items {
      id
      title
      dueDate
    }
  }

  # Order by created date (descending)
  todos(orderBy: "-created_at") {
    items {
      id
      title
      createdAt
    }
  }
}
```

### Get Single TODO

Retrieve a specific TODO by ID.

**Query:**
```graphql
{
  todo(id: "1") {
    id
    title
    description
    dueDate
    isResolved
    createdAt
    updatedAt
  }
}
```

**Response:**
```json
{
  "data": {
    "todo": {
      "id": "1",
      "title": "Complete project",
      "description": "Finish the Django TODO app",
      "dueDate": "2025-12-01T10:00:00+00:00",
      "isResolved": false,
      "createdAt": "2025-11-27T10:00:00+00:00",
      "updatedAt": "2025-11-27T10:00:00+00:00"
    }
  }
}
```

**When TODO doesn't exist:**
```json
{
  "data": {
    "todo": null
  }
}
```

### List Resolved TODOs

Retrieve only resolved TODO items.

**Query:**
```graphql
{
  resolvedTodos(page: 1, pageSize: 10) {
    items {
      id
      title
      isResolved
      createdAt
    }
    pagination {
      total
      hasNext
    }
  }
}
```

### List Unresolved TODOs

Retrieve only unresolved TODO items.

**Query:**
```graphql
{
  unresolvedTodos {
    items {
      id
      title
      dueDate
    }
    pagination {
      total
    }
  }
}
```

### List Overdue TODOs

Retrieve unresolved TODOs with due dates in the past.

**Query:**
```graphql
{
  overdueTodos {
    items {
      id
      title
      dueDate
      isResolved
    }
    pagination {
      total
    }
  }
}
```

### Search TODOs

Search for TODOs by title or description.

**Query:**
```graphql
{
  searchTodos(query: "meeting") {
    items {
      id
      title
      description
    }
    pagination {
      total
    }
  }
}
```

## Mutations

### Create TODO

Create a new TODO item.

**Mutation (Minimal):**
```graphql
mutation {
  createTodo(input: {
    title: "New Task"
  }) {
    success
    message
    todo {
      id
      title
      isResolved
      createdAt
    }
  }
}
```

**Mutation (Full):**
```graphql
mutation {
  createTodo(input: {
    title: "Team Meeting"
    description: "Discuss Q4 objectives and key results"
    dueDate: "2025-12-01T14:00:00Z"
  }) {
    success
    message
    todo {
      id
      title
      description
      dueDate
      isResolved
      createdAt
    }
  }
}
```

**Response (Success):**
```json
{
  "data": {
    "createTodo": {
      "success": true,
      "message": "TODO created successfully.",
      "todo": {
        "id": "2",
        "title": "Team Meeting",
        "description": "Discuss Q4 objectives and key results",
        "dueDate": "2025-12-01T14:00:00+00:00",
        "isResolved": false,
        "createdAt": "2025-11-27T11:00:00+00:00"
      }
    }
  }
}
```

**Response (Validation Error):**
```json
{
  "data": {
    "createTodo": {
      "success": false,
      "message": "Title cannot be empty or whitespace only.",
      "todo": null
    }
  }
}
```

**Using Variables:**
```graphql
mutation CreateTodo($input: TodoInput!) {
  createTodo(input: $input) {
    success
    message
    todo {
      id
      title
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "dueDate": "2025-11-28T10:00:00Z"
  }
}
```

### Update TODO

Update an existing TODO item (partial updates supported).

**Mutation:**
```graphql
mutation {
  updateTodo(
    id: "1"
    input: {
      title: "Updated Title"
      description: "Updated description"
    }
  ) {
    success
    message
    todo {
      id
      title
      description
      updatedAt
    }
  }
}
```

**Update Single Field:**
```graphql
mutation {
  updateTodo(
    id: "1"
    input: { isResolved: true }
  ) {
    success
    message
    todo {
      id
      isResolved
      updatedAt
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "updateTodo": {
      "success": true,
      "message": "TODO updated successfully.",
      "todo": {
        "id": "1",
        "title": "Updated Title",
        "description": "Updated description",
        "updatedAt": "2025-11-27T12:00:00+00:00"
      }
    }
  }
}
```

**Using Variables:**
```graphql
mutation UpdateTodo($id: ID!, $input: TodoUpdateInput!) {
  updateTodo(id: $id, input: $input) {
    success
    message
    todo {
      id
      title
      isResolved
    }
  }
}
```

**Variables:**
```json
{
  "id": "1",
  "input": {
    "title": "New title",
    "isResolved": true
  }
}
```

### Delete TODO

Delete a TODO item permanently.

**Mutation:**
```graphql
mutation {
  deleteTodo(id: "1") {
    success
    message
  }
}
```

**Response:**
```json
{
  "data": {
    "deleteTodo": {
      "success": true,
      "message": "TODO 'Team Meeting' deleted successfully."
    }
  }
}
```

**Using Variables:**
```graphql
mutation DeleteTodo($id: ID!) {
  deleteTodo(id: $id) {
    success
    message
  }
}
```

**Variables:**
```json
{
  "id": "1"
}
```

### Toggle Resolved Status

Toggle the resolved status between true and false.

**Mutation:**
```graphql
mutation {
  toggleResolved(id: "1") {
    success
    message
    todo {
      id
      isResolved
      updatedAt
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "toggleResolved": {
      "success": true,
      "message": "TODO marked as resolved.",
      "todo": {
        "id": "1",
        "isResolved": true,
        "updatedAt": "2025-11-27T12:30:00+00:00"
      }
    }
  }
}
```

### Mark as Resolved

Mark a TODO as resolved.

**Mutation:**
```graphql
mutation {
  markResolved(id: "1") {
    success
    message
    todo {
      id
      isResolved
    }
  }
}
```

### Mark as Unresolved

Mark a TODO as unresolved.

**Mutation:**
```graphql
mutation {
  markUnresolved(id: "1") {
    success
    message
    todo {
      id
      isResolved
    }
  }
}
```

## Advanced Examples

### Combine Multiple Queries

GraphQL allows you to request multiple queries in a single request.

**Query:**
```graphql
{
  # Get all TODOs
  allTodos: todos {
    pagination {
      total
    }
  }

  # Get resolved TODOs
  completed: resolvedTodos {
    pagination {
      total
    }
  }

  # Get unresolved TODOs
  pending: unresolvedTodos {
    pagination {
      total
    }
  }

  # Get overdue TODOs
  overdue: overdueTodos {
    pagination {
      total
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "allTodos": {
      "pagination": { "total": 10 }
    },
    "completed": {
      "pagination": { "total": 4 }
    },
    "pending": {
      "pagination": { "total": 6 }
    },
    "overdue": {
      "pagination": { "total": 2 }
    }
  }
}
```

### Query with Fragments

Use fragments to reuse common field selections.

**Query:**
```graphql
fragment TodoFields on TodoType {
  id
  title
  description
  dueDate
  isResolved
}

{
  todo1: todo(id: "1") {
    ...TodoFields
  }

  todo2: todo(id: "2") {
    ...TodoFields
  }
}
```

### Complex Workflow

Complete workflow: Create, Query, Update, Delete

**Step 1: Create**
```graphql
mutation {
  createTodo(input: {
    title: "Write documentation"
    description: "Document the GraphQL API"
  }) {
    success
    todo {
      id
      title
    }
  }
}
```

**Step 2: Query**
```graphql
{
  todo(id: "3") {
    id
    title
    description
    isResolved
  }
}
```

**Step 3: Update**
```graphql
mutation {
  updateTodo(
    id: "3"
    input: {
      description: "Document the GraphQL API with examples"
      isResolved: true
    }
  ) {
    success
    todo {
      id
      description
      isResolved
    }
  }
}
```

**Step 4: Delete**
```graphql
mutation {
  deleteTodo(id: "3") {
    success
    message
  }
}
```

## Error Handling

### Validation Errors

Returned in the `success` field with a descriptive `message`.

**Example:**
```graphql
mutation {
  createTodo(input: { title: "" }) {
    success
    message
  }
}
```

**Response:**
```json
{
  "data": {
    "createTodo": {
      "success": false,
      "message": "Title cannot be empty or whitespace only."
    }
  }
}
```

### Not Found Errors

**Example:**
```graphql
mutation {
  updateTodo(id: "9999", input: { title: "Test" }) {
    success
    message
  }
}
```

**Response:**
```json
{
  "data": {
    "updateTodo": {
      "success": false,
      "message": "TODO with ID 9999 not found."
    }
  }
}
```

### GraphQL Syntax Errors

**Example (Invalid Syntax):**
```graphql
{
  todos {
    items {
      id
      invalidField
    }
  }
}
```

**Response:**
```json
{
  "errors": [
    {
      "message": "Cannot query field 'invalidField' on type 'TodoType'.",
      "locations": [{"line": 5, "column": 7}]
    }
  ]
}
```

## Client Libraries

### Python with `requests`

```python
import requests

GRAPHQL_URL = "http://localhost:8000/graphql/"

def execute_query(query, variables=None):
    """Execute a GraphQL query."""
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}}
    )
    return response.json()

# Example: List TODOs
query = """
{
  todos {
    items {
      id
      title
      isResolved
    }
  }
}
"""
result = execute_query(query)
print(result)

# Example: Create TODO with variables
mutation = """
mutation CreateTodo($input: TodoInput!) {
  createTodo(input: $input) {
    success
    message
    todo {
      id
      title
    }
  }
}
"""
variables = {
    "input": {
        "title": "New Task",
        "description": "Task details"
    }
}
result = execute_query(mutation, variables)
print(result)
```

### Python with `gql`

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql/",
    headers={"Content-Type": "application/json"}
)

# Create client
client = Client(transport=transport, fetch_schema_from_transport=True)

# Execute query
query = gql("""
    {
      todos {
        items {
          id
          title
        }
      }
    }
""")
result = client.execute(query)
print(result)
```

### JavaScript with Apollo Client

```javascript
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql/',
  cache: new InMemoryCache()
});

// Query
client
  .query({
    query: gql`
      {
        todos {
          items {
            id
            title
            isResolved
          }
        }
      }
    `
  })
  .then(result => console.log(result));

// Mutation
client
  .mutate({
    mutation: gql`
      mutation CreateTodo($input: TodoInput!) {
        createTodo(input: $input) {
          success
          todo {
            id
            title
          }
        }
      }
    `,
    variables: {
      input: {
        title: 'New Task',
        description: 'Task details'
      }
    }
  })
  .then(result => console.log(result));
```

## Testing

### Using Makefile

```bash
# Run GraphQL tests
make test-graphql

# Run all tests
make test
```

### Manual Testing with cURL

```bash
# Create TODO
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createTodo(input: {title: \"Test TODO\"}) { success message todo { id title } } }"
  }' | jq

# List TODOs
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ todos { items { id title } pagination { total } } }"
  }' | jq
```

## Schema Introspection

GraphQL schemas are self-documenting. You can query the schema itself.

**Get All Types:**
```graphql
{
  __schema {
    types {
      name
      kind
      description
    }
  }
}
```

**Get Type Details:**
```graphql
{
  __type(name: "TodoType") {
    name
    kind
    description
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

## Best Practices

### 1. Request Only What You Need

❌ **Bad:**
```graphql
{
  todos {
    items {
      id
      title
      description
      dueDate
      isResolved
      createdAt
      updatedAt
    }
  }
}
```

✅ **Good:**
```graphql
{
  todos {
    items {
      id
      title
      isResolved
    }
  }
}
```

### 2. Use Variables for Dynamic Values

❌ **Bad:**
```graphql
mutation {
  createTodo(input: {title: "Hardcoded Title"}) {
    success
  }
}
```

✅ **Good:**
```graphql
mutation CreateTodo($input: TodoInput!) {
  createTodo(input: $input) {
    success
  }
}
```

### 3. Use Fragments for Repeated Fields

❌ **Bad:**
```graphql
{
  todo1: todo(id: "1") {
    id
    title
    description
  }
  todo2: todo(id: "2") {
    id
    title
    description
  }
}
```

✅ **Good:**
```graphql
fragment TodoInfo on TodoType {
  id
  title
  description
}

{
  todo1: todo(id: "1") { ...TodoInfo }
  todo2: todo(id: "2") { ...TodoInfo }
}
```

### 4. Handle Errors Gracefully

```javascript
const result = await fetch(GRAPHQL_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query })
}).then(res => res.json());

// Check for GraphQL errors
if (result.errors) {
  console.error('GraphQL Errors:', result.errors);
  return;
}

// Check for mutation errors
if (result.data.createTodo && !result.data.createTodo.success) {
  console.error('Mutation failed:', result.data.createTodo.message);
  return;
}

// Process successful result
console.log('Success:', result.data);
```

## Comparison: GraphQL vs REST

### REST API
```bash
# Multiple requests needed
GET /api/todos/              # Get list
GET /api/todos/1/            # Get details
GET /api/todos/resolved/     # Get resolved
GET /api/todos/overdue/      # Get overdue
```

### GraphQL API
```graphql
# Single request
{
  all: todos { pagination { total } }
  details: todo(id: "1") { title description }
  resolved: resolvedTodos { pagination { total } }
  overdue: overdueTodos { pagination { total } }
}
```

## Additional Resources

- [GraphiQL Interface](http://localhost:8000/graphql/) - Interactive documentation
- [Strawberry GraphQL Docs](https://strawberry.rocks/docs)
- [GraphQL Official Docs](https://graphql.org/learn/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

## Support

For issues with the GraphQL API:
1. Check this guide
2. Use the GraphiQL interface for schema exploration
3. Run tests: `make test-graphql`
4. Check Django logs: `make logs`
