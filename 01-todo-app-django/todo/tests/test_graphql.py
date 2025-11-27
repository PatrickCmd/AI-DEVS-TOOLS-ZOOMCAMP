"""
Tests for the TODO GraphQL API.

This module contains comprehensive tests for all GraphQL queries and mutations
including filtering, searching, pagination, and error handling.
"""

import pytest
from django.utils import timezone
from datetime import timedelta

from todo.models import Todo
from todo.graphql.schema import schema


def execute_query(query, variables=None):
    """Helper function to execute GraphQL queries."""
    return schema.execute_sync(query, variable_values=variables or {})


@pytest.fixture
def sample_todo():
    """Fixture for creating a sample TODO."""
    return Todo.objects.create(
        title="Test TODO",
        description="Test description",
        due_date=timezone.now() + timedelta(days=1)
    )


@pytest.fixture
def multiple_todos():
    """Fixture for creating multiple TODOs."""
    todos = []
    for i in range(5):
        todo = Todo.objects.create(
            title=f"TODO {i}",
            description=f"Description {i}",
            is_resolved=(i % 2 == 0)
        )
        todos.append(todo)
    return todos


@pytest.fixture
def overdue_todo():
    """Fixture for creating an overdue TODO."""
    return Todo.objects.create(
        title="Overdue TODO",
        description="This is overdue",
        due_date=timezone.now() - timedelta(days=1),
        is_resolved=False
    )


@pytest.mark.django_db
class TestGraphQLQueries:
    """Tests for GraphQL queries."""

    def test_todos_query_empty(self):
        """Test querying TODOs when none exist."""
        query = """
            query {
                todos {
                    items {
                        id
                        title
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todos"]["pagination"]["total"] == 0
        assert result.data["todos"]["items"] == []

    def test_todos_query(self, multiple_todos):
        """Test querying all TODOs."""
        query = """
            query {
                todos {
                    items {
                        id
                        title
                        description
                        isResolved
                    }
                    pagination {
                        total
                        page
                        pageSize
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todos"]["pagination"]["total"] == 5
        assert len(result.data["todos"]["items"]) == 5

    def test_todos_query_with_filter(self, multiple_todos):
        """Test querying TODOs with resolved filter."""
        query = """
            query {
                todos(isResolved: true) {
                    items {
                        id
                        isResolved
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        # 3 out of 5 are resolved (0, 2, 4)
        assert result.data["todos"]["pagination"]["total"] == 3
        for item in result.data["todos"]["items"]:
            assert item["isResolved"] is True

    def test_todos_query_with_search(self):
        """Test querying TODOs with search."""
        Todo.objects.create(title="Buy groceries", description="Milk and eggs")
        Todo.objects.create(title="Doctor appointment", description="Check-up")

        query = """
            query {
                todos(search: "groceries") {
                    items {
                        title
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todos"]["pagination"]["total"] == 1
        assert "groceries" in result.data["todos"]["items"][0]["title"].lower()

    def test_todos_query_with_pagination(self):
        """Test TODO pagination."""
        # Create 15 TODOs
        for i in range(15):
            Todo.objects.create(title=f"TODO {i}", description=f"Description {i}")

        query = """
            query {
                todos(page: 1, pageSize: 10) {
                    items {
                        title
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
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todos"]["pagination"]["total"] == 15
        assert len(result.data["todos"]["items"]) == 10
        assert result.data["todos"]["pagination"]["hasNext"] is True
        assert result.data["todos"]["pagination"]["hasPrevious"] is False

    def test_todo_query_by_id(self, sample_todo):
        """Test querying a single TODO by ID."""
        query = f"""
            query {{
                todo(id: "{sample_todo.id}") {{
                    id
                    title
                    description
                    isResolved
                }}
            }}
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todo"]["id"] == str(sample_todo.id)
        assert result.data["todo"]["title"] == sample_todo.title

    def test_todo_query_not_found(self):
        """Test querying a TODO that doesn't exist."""
        query = """
            query {
                todo(id: "9999") {
                    id
                    title
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["todo"] is None

    def test_resolved_todos_query(self, multiple_todos):
        """Test resolved TODOs query."""
        query = """
            query {
                resolvedTodos {
                    items {
                        id
                        isResolved
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        # 3 out of 5 are resolved
        assert result.data["resolvedTodos"]["pagination"]["total"] == 3

    def test_unresolved_todos_query(self, multiple_todos):
        """Test unresolved TODOs query."""
        query = """
            query {
                unresolvedTodos {
                    items {
                        id
                        isResolved
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        # 2 out of 5 are unresolved
        assert result.data["unresolvedTodos"]["pagination"]["total"] == 2

    def test_overdue_todos_query(self, overdue_todo):
        """Test overdue TODOs query."""
        # Create a non-overdue TODO
        Todo.objects.create(
            title="Not overdue",
            due_date=timezone.now() + timedelta(days=1),
            is_resolved=False
        )

        query = """
            query {
                overdueTodos {
                    items {
                        title
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        # Only the overdue TODO
        assert result.data["overdueTodos"]["pagination"]["total"] == 1
        assert result.data["overdueTodos"]["items"][0]["title"] == "Overdue TODO"

    def test_search_todos_query(self):
        """Test search TODOs query."""
        Todo.objects.create(title="Python programming", description="Learn Django")
        Todo.objects.create(title="JavaScript coding", description="Learn React")

        query = """
            query {
                searchTodos(query: "Python") {
                    items {
                        title
                    }
                    pagination {
                        total
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert result.data["searchTodos"]["pagination"]["total"] == 1
        assert "Python" in result.data["searchTodos"]["items"][0]["title"]


@pytest.mark.django_db
class TestGraphQLMutations:
    """Tests for GraphQL mutations."""

    def test_create_todo_minimal(self):
        """Test creating a TODO with minimal fields."""
        mutation = """
            mutation {
                createTodo(input: {title: "New TODO"}) {
                    success
                    message
                    todo {
                        title
                        description
                        isResolved
                    }
                }
            }
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["createTodo"]["success"] is True
        assert result.data["createTodo"]["todo"]["title"] == "New TODO"
        assert result.data["createTodo"]["todo"]["isResolved"] is False
        assert Todo.objects.count() == 1

    def test_create_todo_full(self):
        """Test creating a TODO with all fields."""
        due_date = (timezone.now() + timedelta(days=7)).isoformat()
        mutation = f"""
            mutation {{
                createTodo(input: {{
                    title: "Complete TODO",
                    description: "Full description",
                    dueDate: "{due_date}"
                }}) {{
                    success
                    message
                    todo {{
                        title
                        description
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["createTodo"]["success"] is True
        assert result.data["createTodo"]["todo"]["title"] == "Complete TODO"
        assert result.data["createTodo"]["todo"]["description"] == "Full description"

    def test_create_todo_empty_title(self):
        """Test creating a TODO with empty title fails."""
        mutation = """
            mutation {
                createTodo(input: {title: ""}) {
                    success
                    message
                    todo {
                        title
                    }
                }
            }
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["createTodo"]["success"] is False
        assert "empty" in result.data["createTodo"]["message"].lower()

    def test_create_todo_past_due_date(self):
        """Test creating a TODO with past due date fails."""
        past_date = (timezone.now() - timedelta(days=1)).isoformat()
        mutation = f"""
            mutation {{
                createTodo(input: {{
                    title: "Past TODO",
                    dueDate: "{past_date}"
                }}) {{
                    success
                    message
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["createTodo"]["success"] is False
        assert "past" in result.data["createTodo"]["message"].lower()

    def test_update_todo(self, sample_todo):
        """Test updating a TODO."""
        mutation = f"""
            mutation {{
                updateTodo(
                    id: "{sample_todo.id}",
                    input: {{title: "Updated Title"}}
                ) {{
                    success
                    message
                    todo {{
                        title
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["updateTodo"]["success"] is True
        assert result.data["updateTodo"]["todo"]["title"] == "Updated Title"

        sample_todo.refresh_from_db()
        assert sample_todo.title == "Updated Title"

    def test_update_todo_not_found(self):
        """Test updating a TODO that doesn't exist."""
        mutation = """
            mutation {
                updateTodo(
                    id: "9999",
                    input: {title: "Updated"}
                ) {
                    success
                    message
                }
            }
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["updateTodo"]["success"] is False
        assert "not found" in result.data["updateTodo"]["message"].lower()

    def test_delete_todo(self, sample_todo):
        """Test deleting a TODO."""
        mutation = f"""
            mutation {{
                deleteTodo(id: "{sample_todo.id}") {{
                    success
                    message
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["deleteTodo"]["success"] is True
        assert Todo.objects.count() == 0

    def test_delete_todo_not_found(self):
        """Test deleting a TODO that doesn't exist."""
        mutation = """
            mutation {
                deleteTodo(id: "9999") {
                    success
                    message
                }
            }
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["deleteTodo"]["success"] is False
        assert "not found" in result.data["deleteTodo"]["message"].lower()

    def test_toggle_resolved(self, sample_todo):
        """Test toggling resolved status."""
        assert sample_todo.is_resolved is False

        mutation = f"""
            mutation {{
                toggleResolved(id: "{sample_todo.id}") {{
                    success
                    message
                    todo {{
                        isResolved
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["toggleResolved"]["success"] is True
        assert result.data["toggleResolved"]["todo"]["isResolved"] is True

        sample_todo.refresh_from_db()
        assert sample_todo.is_resolved is True

    def test_mark_resolved(self, sample_todo):
        """Test marking TODO as resolved."""
        mutation = f"""
            mutation {{
                markResolved(id: "{sample_todo.id}") {{
                    success
                    todo {{
                        isResolved
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["markResolved"]["success"] is True
        assert result.data["markResolved"]["todo"]["isResolved"] is True

    def test_mark_unresolved(self):
        """Test marking TODO as unresolved."""
        todo = Todo.objects.create(title="Test", is_resolved=True)

        mutation = f"""
            mutation {{
                markUnresolved(id: "{todo.id}") {{
                    success
                    todo {{
                        isResolved
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["markUnresolved"]["success"] is True
        assert result.data["markUnresolved"]["todo"]["isResolved"] is False


@pytest.mark.django_db
class TestGraphQLComplexScenarios:
    """Tests for complex GraphQL scenarios."""

    def test_create_and_query(self):
        """Test creating a TODO and then querying it."""
        # Create
        create_mutation = """
            mutation {
                createTodo(input: {title: "Test TODO"}) {
                    success
                    todo {
                        id
                        title
                    }
                }
            }
        """
        create_result = execute_query(create_mutation)
        assert create_result.errors is None
        todo_id = create_result.data["createTodo"]["todo"]["id"]

        # Query
        query = f"""
            query {{
                todo(id: "{todo_id}") {{
                    id
                    title
                }}
            }}
        """
        query_result = execute_query(query)
        assert query_result.errors is None
        assert query_result.data["todo"]["title"] == "Test TODO"

    def test_update_multiple_fields(self, sample_todo):
        """Test updating multiple fields at once."""
        mutation = f"""
            mutation {{
                updateTodo(
                    id: "{sample_todo.id}",
                    input: {{
                        title: "New Title",
                        description: "New Description",
                        isResolved: true
                    }}
                ) {{
                    success
                    todo {{
                        title
                        description
                        isResolved
                    }}
                }}
            }}
        """
        result = execute_query(mutation)
        assert result.errors is None
        assert result.data["updateTodo"]["success"] is True
        assert result.data["updateTodo"]["todo"]["title"] == "New Title"
        assert result.data["updateTodo"]["todo"]["description"] == "New Description"
        assert result.data["updateTodo"]["todo"]["isResolved"] is True

    def test_pagination_second_page(self):
        """Test querying second page of results."""
        # Create 15 TODOs
        for i in range(15):
            Todo.objects.create(title=f"TODO {i}")

        query = """
            query {
                todos(page: 2, pageSize: 10) {
                    items {
                        title
                    }
                    pagination {
                        page
                        hasNext
                        hasPrevious
                    }
                }
            }
        """
        result = execute_query(query)
        assert result.errors is None
        assert len(result.data["todos"]["items"]) == 5
        assert result.data["todos"]["pagination"]["hasNext"] is False
        assert result.data["todos"]["pagination"]["hasPrevious"] is True
