# Makefile for Django Template

.PHONY: install migrate run test clean createsuperuser-admin createsuperuser seed seed-clear

install:
	uv sync --dev

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

# Idempotent, non-interactive: creates/updates admin (username=admin, email=admin@example.com) and sets password.
createsuperuser-admin:
	uv run python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u,created=User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True}); u.email='admin@example.com'; u.is_staff=True; u.is_superuser=True; u.set_password('admin123'); u.save(); print('created' if created else 'updated')"

# Interactive (recommended for real deployments). Example:
# make createsuperuser ARGS="--username admin --email admin@example.com"
createsuperuser:
	uv run python manage.py createsuperuser $(ARGS)

# Seed synthetic pets + products 🐾🛒
# Examples:
#   make seed
#   make seed SEED=42
#   make seed PETS=30 PRODUCTS=40 SEED=7
seed:
	uv run python manage.py seed_store $(if $(PETS),--pets $(PETS),) $(if $(PRODUCTS),--products $(PRODUCTS),) $(if $(SEED),--seed $(SEED),)

# Seed after clearing existing rows (handy during development)
# Examples:
#   make seed-clear
#   make seed-clear SEED=42
seed-clear:
	uv run python manage.py seed_store --clear $(if $(PETS),--pets $(PETS),) $(if $(PRODUCTS),--products $(PRODUCTS),) $(if $(SEED),--seed $(SEED),)

run:
	uv run python manage.py runserver

test:
	uv run python manage.py test

clean:
	rm -rf __pycache__ myapp/__pycache__ myproject/__pycache__
	rm -rf db.sqlite3
