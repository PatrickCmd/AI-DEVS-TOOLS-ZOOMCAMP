# Makefile Guide

## Overview
The `Makefile` provides convenient shortcuts for all common development tasks. Instead of typing long Docker Compose commands, you can use simple `make` commands.

## Quick Reference

### 🚀 Getting Started
```bash
make setup          # Complete setup (build, migrate, create superuser, start)
make quickstart     # Show quick start guide
make help           # Show all available commands
```

### 📦 Docker Management
```bash
make build          # Build Docker containers
make up             # Start all services
make down           # Stop all services
make restart        # Restart all services
make ps             # Show running containers
make logs           # View web service logs
make logs-all       # View all service logs
```

### 🗄️ Database Operations
```bash
make migrate               # Run migrations
make makemigrations        # Create new migrations
make showmigrations        # Show migration status
make createsuperuser       # Create admin user (admin/admin123)
make reset-db             # Reset database (destroys all data!)
```

### 🧪 Testing Commands
```bash
make test                  # Run all tests
make test-v                # Run tests (verbose)
make test-vv               # Run tests (very verbose)
make test-cov              # Run tests with coverage report
make coverage-html         # Generate and open HTML coverage report

# Test specific modules
make test-models           # Run model tests only
make test-views            # Run view tests only
make test-urls             # Run URL tests only
make test-templates        # Run template tests only
make test-markdown         # Run markdown tests only
make test-failed           # Re-run only failed tests
```

### 🛠️ Development Tools
```bash
make shell             # Open Django shell
make dbshell           # Open database shell
make bash              # Open bash shell in web container
make check             # Run Django system checks
make collectstatic     # Collect static files
```

### 📦 Installation
```bash
make install           # Install dependencies locally
make install-frozen    # Install from lock file
```

### 🧹 Cleanup
```bash
make clean             # Remove containers, volumes, and cache
make clean-cache       # Remove Python cache files only
```

### 🔄 Aliases
```bash
make run               # Same as 'make up'
make stop              # Same as 'make down'
make dev               # Start with logs (development mode)
```

### 📊 Utilities
```bash
make version           # Show version information
make ci-test           # Run tests in CI mode (with XML output)
```

## Common Workflows

### First Time Setup
```bash
# Clone the repository
git clone <repo-url>
cd 01-todo-app-django

# Complete setup (builds, migrates, creates admin)
make setup

# Access the app
# http://localhost:8000
# Admin: http://localhost:8000/admin (admin/admin123)
```

### Daily Development
```bash
# Start your day
make up              # Start services
make logs            # View logs (optional)

# Make changes to code...

# Test your changes
make test-v          # Run tests with verbose output

# Check specific functionality
make test-views      # Test views only

# Stop at end of day
make down
```

### Database Changes
```bash
# After modifying models.py
make makemigrations  # Create migration files
make migrate         # Apply migrations

# Check migration status
make showmigrations

# If you need to reset (WARNING: destroys data!)
make reset-db
```

### Testing Workflow
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# View coverage report in browser
make coverage-html

# Run specific test file
make test-markdown

# Only re-run failed tests
make test-failed
```

### Debugging
```bash
# View logs
make logs

# Open Django shell to test code
make shell

# Open database shell
make dbshell

# Check for issues
make check

# Open bash in container
make bash
```

### Cleanup and Reset
```bash
# Clean cache files
make clean-cache

# Full cleanup (removes containers and volumes)
make clean

# Reset database with fresh data
make reset-db
```

## Command Details

### `make setup`
Complete first-time setup including:
1. Build Docker containers
2. Run database migrations
3. Create superuser (admin/admin123)
4. Start all services

**When to use:** First time setting up the project

### `make up`
Start all services (web + database) in detached mode.

**When to use:** Daily development start

### `make down`
Stop all running services.

**When to use:** End of work session

### `make test-cov`
Run complete test suite with coverage analysis.

**Output:**
- Terminal coverage summary
- HTML coverage report in `htmlcov/`

**When to use:** Before committing code

### `make migrate`
Apply database migrations.

**When to use:** After pulling new code or creating migrations

### `make makemigrations`
Create new migration files based on model changes.

**When to use:** After modifying models.py

### `make shell`
Open Django interactive shell.

**When to use:** Testing Django ORM queries, debugging

### `make reset-db`
⚠️ **WARNING:** Destroys all data!

Completely resets the database:
1. Stops and removes containers/volumes
2. Starts fresh database
3. Runs migrations
4. Creates new superuser

**When to use:** Starting fresh, clearing test data

### `make logs`
View real-time logs from web service.

**When to use:** Debugging, monitoring requests

**Tip:** Press `Ctrl+C` to exit

### `make version`
Display version information for:
- Python
- Django
- PostgreSQL

**When to use:** Debugging environment issues

## Color Output

The Makefile uses colored output for better readability:
- 🔵 **Blue** - Information messages
- 🟢 **Green** - Success messages
- 🟡 **Yellow** - Warning messages
- 🔴 **Red** - Error/danger messages

## Tips and Best Practices

### 1. Always check status before starting
```bash
make ps  # See what's already running
```

### 2. View logs when debugging
```bash
make logs  # Keep this running in a separate terminal
```

### 3. Run tests before committing
```bash
make test-cov  # Ensure 99% coverage is maintained
```

### 4. Clean up regularly
```bash
make clean-cache  # Remove Python cache files
```

### 5. Use specific test commands for speed
```bash
# Instead of running all tests
make test-views  # Only test what you changed
```

### 6. Check before deploying
```bash
make check      # Django system checks
make test-cov   # Full test suite
make ci-test    # CI-mode tests
```

## Troubleshooting

### "Port already in use"
```bash
make down           # Stop services
make ps             # Verify nothing running
make up             # Start again
```

### "Database connection failed"
```bash
make logs           # Check for database errors
make restart        # Restart services
```

### "Tests failing"
```bash
make test-v         # Verbose output for details
make test-failed    # Re-run only failed tests
make reset-db       # Last resort - reset database
```

### "Permission denied"
```bash
# On Linux, may need to add user to docker group
sudo usermod -aG docker $USER
# Then log out and back in
```

## CI/CD Integration

For continuous integration:
```bash
make ci-test
```

This runs tests with XML output suitable for CI systems like:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

## Adding Custom Commands

To add your own commands, edit the Makefile:

```makefile
my-command: ## Description of my command
	@echo "Running my command..."
	docker compose run --rm web uv run python manage.py my_command
```

The `## Description` part appears in `make help`.

## Performance Tips

### Faster Test Runs
```bash
# Use pytest's cache to skip slow tests
make test-failed

# Run specific test file
make test-models
```

### Faster Startup
```bash
# Use cached builds
make up  # Doesn't rebuild unless needed

# Force rebuild only when necessary
make build
```

## Environment Variables

The Makefile uses variables from `.env`:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `DEBUG`

Edit `.env` to customize these values.

## Dependencies

Required tools:
- ✅ Docker
- ✅ Docker Compose
- ✅ Make (usually pre-installed on Unix systems)

Optional:
- `uv` (for local development without Docker)

## Further Reading

- [README.md](README.md) - Project overview
- [MARKDOWN_GUIDE.md](MARKDOWN_GUIDE.md) - Markdown features
- [DATE_PICKER_GUIDE.md](DATE_PICKER_GUIDE.md) - Date picker usage
- [FEATURE_SUMMARY.md](FEATURE_SUMMARY.md) - Recent enhancements

## Support

For help:
```bash
make help        # Show all commands
make quickstart  # Quick start guide
```
