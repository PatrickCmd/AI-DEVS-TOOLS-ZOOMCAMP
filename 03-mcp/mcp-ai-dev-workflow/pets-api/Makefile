.PHONY: help build up down restart logs shell db-shell migrate makemigrations createsuperuser test test-cov clean lint format check install

# Default target
help:
	@echo "Petstore API - Available Commands"
	@echo "=================================="
	@echo "Docker Commands:"
	@echo "  make build              - Build Docker containers"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make restart            - Restart all services"
	@echo "  make logs               - View container logs"
	@echo "  make logs-backend       - View backend logs only"
	@echo "  make logs-db            - View database logs only"
	@echo ""
	@echo "Django Commands:"
	@echo "  make shell              - Open Django shell"
	@echo "  make bash               - Open bash shell in backend container"
	@echo "  make db-shell           - Open PostgreSQL shell"
	@echo "  make migrate            - Run database migrations"
	@echo "  make makemigrations     - Create new migrations"
	@echo "  make createsuperuser    - Create Django superuser"
	@echo "  make collectstatic      - Collect static files"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test               - Run all tests"
	@echo "  make test-cov           - Run tests with coverage report"
	@echo "  make test-models        - Run model tests only"
	@echo "  make test-views         - Run view tests only"
	@echo "  make test-admin         - Run admin tests only"
	@echo "  make test-users         - Run user app tests"
	@echo "  make test-pets          - Run pets app tests"
	@echo "  make test-store         - Run store app tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint               - Run ruff linter"
	@echo "  make lint-all           - Run all linters (ruff, flake8, pylint)"
	@echo "  make format             - Format code (black + isort)"
	@echo "  make format-check       - Check code formatting without making changes"
	@echo "  make check              - Run type checking (mypy)"
	@echo "  make security           - Run security checks (bandit)"
	@echo "  make quality            - Run all quality checks"
	@echo ""
	@echo "Development:"
	@echo "  make install            - Install dependencies locally"
	@echo "  make shell-plus         - Open enhanced Django shell with shell_plus"
	@echo "  make show-urls          - Show all URL patterns"
	@echo "  make graph-models       - Generate model diagrams (requires graphviz)"
	@echo "  make clean              - Clean up containers and volumes"
	@echo "  make reset-db           - Reset database (WARNING: deletes all data)"
	@echo "  make seed-data          - Seed database with sample data"
	@echo ""
	@echo "Fixture Management:"
	@echo "  make dump-fixtures      - Export all data to fixtures"
	@echo "  make dump-pets          - Export pets app data to fixtures"
	@echo "  make dump-users         - Export users app data to fixtures"
	@echo "  make dump-store         - Export store app data to fixtures"
	@echo "  make load-fixtures      - Load all fixtures into database"
	@echo "  make create-sample      - Create sample fixtures for testing"

# Docker commands
build:
	docker compose build

up:
	docker compose up -d
	@echo "Waiting for services to start..."
	@sleep 3
	@echo "Services are up! Access the API at http://localhost:8000"
	@echo "Admin panel: http://localhost:8000/admin/"
	@echo "API Docs: http://localhost:8000/api/docs/"

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-db:
	docker compose logs -f db

# Django commands
shell:
	docker compose exec backend python src/manage.py shell

bash:
	docker compose exec backend bash

db-shell:
	docker compose exec db psql -U petstore -d petstore_db

migrate:
	docker compose exec backend python src/manage.py migrate

makemigrations:
	docker compose exec backend python src/manage.py makemigrations

createsuperuser:
	docker compose exec backend python src/manage.py createsuperuser

collectstatic:
	docker compose exec backend python src/manage.py collectstatic --noinput

# Testing commands
test:
	docker compose exec backend pytest src/ -v

test-cov:
	docker compose exec backend pytest src/ -v --cov=src --cov-report=term-missing --cov-report=html

test-models:
	docker compose exec backend pytest src/ -v -k "test_models"

test-views:
	docker compose exec backend pytest src/ -v -k "test_views"

test-admin:
	docker compose exec backend pytest src/ -v -k "test_admin"

test-users:
	docker compose exec backend pytest src/users/tests/ -v

test-pets:
	docker compose exec backend pytest src/pets/tests/ -v

test-store:
	docker compose exec backend pytest src/store/tests/ -v

# Code quality
lint:
	@echo "Running ruff linter..."
	docker compose exec backend ruff check src/

lint-all:
	@echo "Running all linters..."
	@echo "\n=== Ruff ==="
	docker compose exec backend ruff check src/
	@echo "\n=== Flake8 ==="
	docker compose exec backend flake8 src/
	@echo "\n=== Pylint ==="
	docker compose exec backend pylint src/*/

format:
	@echo "Formatting code with black and isort..."
	docker compose exec backend black src/
	docker compose exec backend isort src/
	@echo "Code formatting completed!"

format-check:
	@echo "Checking code formatting..."
	docker compose exec backend black --check src/
	docker compose exec backend isort --check-only src/

check:
	@echo "Running type checks with mypy..."
	docker compose exec backend mypy src/

security:
	@echo "Running security checks with bandit..."
	docker compose exec backend bandit -r src/ -ll

quality: lint-all check security
	@echo "\nAll code quality checks completed!"

# Development
install:
	uv pip install -e ".[dev]"

shell-plus:
	docker compose exec backend python src/manage.py shell_plus

show-urls:
	docker compose exec backend python src/manage.py show_urls

graph-models:
	@mkdir -p docs/diagrams
	docker compose exec backend python src/manage.py graph_models -a -g -o docs/diagrams/models.png
	@echo "Model diagram saved to docs/diagrams/models.png"

clean:
	docker compose down -v
	rm -rf htmlcov .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

reset-db:
	docker compose exec db psql -U petstore -d petstore_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker compose exec backend python src/manage.py migrate
	@echo "Database has been reset!"

seed-data:
	docker compose exec backend python src/manage.py shell -c "from pets.models import Category, Tag; Category.objects.get_or_create(name='Dogs'); Category.objects.get_or_create(name='Cats'); Tag.objects.get_or_create(name='friendly'); Tag.objects.get_or_create(name='playful');"
	@echo "Sample data seeded!"

# First time setup
setup: build up migrate seed-data
	@echo ""
	@echo "Setup complete! Now create a superuser:"
	@echo "  make createsuperuser"

# Fixture management
dump-fixtures:
	@mkdir -p fixtures
	@echo "Exporting all fixtures..."
	docker compose exec backend python src/manage.py dumpdata pets.Category pets.Tag --indent 2 --output fixtures/pets_categories_tags.json
	docker compose exec backend python src/manage.py dumpdata pets.Pet --indent 2 --output fixtures/pets_pets.json
	docker compose exec backend python src/manage.py dumpdata users.User --indent 2 --output fixtures/users.json
	docker compose exec backend python src/manage.py dumpdata store.Order --indent 2 --output fixtures/store_orders.json
	@echo "Fixtures exported to fixtures/ directory"

dump-pets:
	@mkdir -p fixtures
	docker compose exec backend python src/manage.py dumpdata pets --indent 2 --output fixtures/pets.json
	@echo "Pets app fixtures exported to fixtures/pets.json"

dump-users:
	@mkdir -p fixtures
	docker compose exec backend python src/manage.py dumpdata users --indent 2 --output fixtures/users.json
	@echo "Users app fixtures exported to fixtures/users.json"

dump-store:
	@mkdir -p fixtures
	docker compose exec backend python src/manage.py dumpdata store --indent 2 --output fixtures/store.json
	@echo "Store app fixtures exported to fixtures/store.json"

load-fixtures:
	@echo "Loading fixtures into database..."
	@if [ -f fixtures/users.json ]; then \
		docker compose exec backend python src/manage.py loaddata fixtures/users.json; \
	fi
	@if [ -f fixtures/pets_categories_tags.json ]; then \
		docker compose exec backend python src/manage.py loaddata fixtures/pets_categories_tags.json; \
	fi
	@if [ -f fixtures/pets_pets.json ]; then \
		docker compose exec backend python src/manage.py loaddata fixtures/pets_pets.json; \
	fi
	@if [ -f fixtures/store_orders.json ]; then \
		docker compose exec backend python src/manage.py loaddata fixtures/store_orders.json; \
	fi
	@echo "Fixtures loaded successfully!"

create-sample:
	@mkdir -p fixtures
	@echo "Creating sample fixtures..."
	@echo '[\n  {\n    "model": "pets.category",\n    "pk": 1,\n    "fields": {\n      "name": "Dogs"\n    }\n  },\n  {\n    "model": "pets.category",\n    "pk": 2,\n    "fields": {\n      "name": "Cats"\n    }\n  },\n  {\n    "model": "pets.category",\n    "pk": 3,\n    "fields": {\n      "name": "Birds"\n    }\n  },\n  {\n    "model": "pets.tag",\n    "pk": 1,\n    "fields": {\n      "name": "friendly"\n    }\n  },\n  {\n    "model": "pets.tag",\n    "pk": 2,\n    "fields": {\n      "name": "playful"\n    }\n  },\n  {\n    "model": "pets.tag",\n    "pk": 3,\n    "fields": {\n      "name": "calm"\n    }\n  },\n  {\n    "model": "pets.tag",\n    "pk": 4,\n    "fields": {\n      "name": "trained"\n    }\n  }\n]' > fixtures/sample_categories_tags.json
	docker compose exec backend python src/manage.py loaddata fixtures/sample_categories_tags.json
	@echo "Sample fixtures created and loaded!"
