.PHONY: help build up down restart logs shell test test-v test-cov migrate makemigrations createsuperuser clean install check format lint

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Django TODO App - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Docker Commands
build: ## Build Docker containers
	@echo "$(BLUE)Building Docker containers...$(NC)"
	docker compose build

up: ## Start all services
	@echo "$(GREEN)Starting services...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Services started! App available at http://localhost:8000$(NC)"

down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker compose down

restart: ## Restart all services
	@echo "$(YELLOW)Restarting services...$(NC)"
	docker compose restart

logs: ## View logs from web service
	docker compose logs -f web

logs-all: ## View logs from all services
	docker compose logs -f

ps: ## Show running containers
	docker compose ps

# Development Commands
shell: ## Open Django shell
	docker compose run --rm web uv run python manage.py shell

dbshell: ## Open database shell
	docker compose run --rm web uv run python manage.py dbshell

bash: ## Open bash shell in web container
	docker compose exec web bash

# Database Commands
migrate: ## Run database migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	docker compose run --rm web uv run python manage.py migrate

makemigrations: ## Create new migrations
	@echo "$(BLUE)Creating migrations...$(NC)"
	docker compose run --rm web uv run python manage.py makemigrations

showmigrations: ## Show migration status
	docker compose run --rm web uv run python manage.py showmigrations

createsuperuser: ## Create a superuser
	docker compose run --rm web uv run python create_superuser.py

# Testing Commands
test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	docker compose run --rm web uv run pytest

test-v: ## Run tests with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	docker compose run --rm web uv run pytest -v

test-vv: ## Run tests with very verbose output
	docker compose run --rm web uv run pytest -vv

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	docker compose run --rm web uv run pytest --cov=todo --cov-report=html --cov-report=term-missing

test-models: ## Run model tests only
	docker compose run --rm web uv run pytest todo/tests/test_models.py -v

test-views: ## Run view tests only
	docker compose run --rm web uv run pytest todo/tests/test_views.py -v

test-urls: ## Run URL tests only
	docker compose run --rm web uv run pytest todo/tests/test_urls.py -v

test-templates: ## Run template tests only
	docker compose run --rm web uv run pytest todo/tests/test_templates.py -v

test-markdown: ## Run markdown tests only
	docker compose run --rm web uv run pytest todo/tests/test_markdown.py -v

test-api: ## Run API tests only
	docker compose run --rm web uv run pytest todo/tests/test_api.py -v

test-graphql: ## Run GraphQL tests only
	docker compose run --rm web uv run pytest todo/tests/test_graphql.py -v

test-failed: ## Re-run only failed tests
	docker compose run --rm web uv run pytest --lf

# Installation Commands
install: ## Install dependencies locally
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync --no-build-isolation

install-frozen: ## Install dependencies from lock file
	@echo "$(BLUE)Installing dependencies from lock file...$(NC)"
	uv sync --frozen --no-build-isolation

# Code Quality Commands
check: ## Run Django system checks
	docker compose run --rm web uv run python manage.py check

format: ## Format code (placeholder - add black/ruff if needed)
	@echo "$(YELLOW)Code formatting not configured. Add black or ruff to format code.$(NC)"

lint: ## Lint code (placeholder - add pylint/ruff if needed)
	@echo "$(YELLOW)Linting not configured. Add pylint or ruff to lint code.$(NC)"

# Cleanup Commands
clean: ## Remove containers, volumes, and cached files
	@echo "$(RED)Cleaning up...$(NC)"
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-cache: ## Remove Python cache files
	@echo "$(YELLOW)Removing Python cache files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Complete Setup Commands
setup: build migrate createsuperuser up ## Complete setup: build, migrate, create superuser, and start
	@echo "$(GREEN)Setup complete! App available at http://localhost:8000$(NC)"
	@echo "$(GREEN)Admin: http://localhost:8000/admin (admin/admin123)$(NC)"

dev: up logs ## Start in development mode with logs

# Quick Commands
run: up ## Alias for 'up'

stop: down ## Alias for 'down'

# Database Reset
reset-db: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(RED)Resetting database...$(NC)"; \
		docker compose down -v; \
		docker compose up -d db; \
		sleep 5; \
		docker compose run --rm web uv run python manage.py migrate; \
		docker compose run --rm web uv run python create_superuser.py; \
		docker compose up -d; \
		echo "$(GREEN)Database reset complete!$(NC)"; \
	else \
		echo "$(YELLOW)Database reset cancelled.$(NC)"; \
	fi

# Coverage Report
coverage-html: test-cov ## Generate and open HTML coverage report
	@echo "$(GREEN)Opening coverage report...$(NC)"
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "Open htmlcov/index.html manually"

# CI/CD Commands
ci-test: ## Run tests in CI mode
	docker compose run --rm web uv run pytest -v --cov=todo --cov-report=xml --cov-report=term

# Utility Commands
version: ## Show versions
	@echo "$(BLUE)Version Information:$(NC)"
	@echo "Python: $$(docker compose run --rm web python --version 2>&1 | grep -o 'Python.*')"
	@echo "Django: $$(docker compose run --rm web uv run python -c 'import django; print(django.get_version())' 2>&1 | tail -1)"
	@echo "PostgreSQL: $$(docker compose exec db psql --version 2>&1 | grep -o 'psql.*')"

collectstatic: ## Collect static files
	docker compose run --rm web uv run python manage.py collectstatic --noinput

# Quick Start Guide
quickstart: ## Show quick start guide
	@echo "$(BLUE)Quick Start Guide$(NC)"
	@echo ""
	@echo "$(GREEN)1. First Time Setup:$(NC)"
	@echo "   make setup"
	@echo ""
	@echo "$(GREEN)2. Daily Development:$(NC)"
	@echo "   make up        # Start services"
	@echo "   make logs      # View logs"
	@echo "   make test      # Run tests"
	@echo "   make down      # Stop services"
	@echo ""
	@echo "$(GREEN)3. Database Changes:$(NC)"
	@echo "   make makemigrations"
	@echo "   make migrate"
	@echo ""
	@echo "$(GREEN)4. Access Points:$(NC)"
	@echo "   App:   http://localhost:8000"
	@echo "   Admin: http://localhost:8000/admin"
	@echo ""
	@echo "$(YELLOW)For more commands, run: make help$(NC)"
