# Code Quality & Linting Guide

Comprehensive guide to code quality tools, linting, formatting, and development utilities configured for this project.

## Table of Contents

- [Overview](#overview)
- [Linting Tools](#linting-tools)
- [Code Formatting](#code-formatting)
- [Type Checking](#type-checking)
- [Security Scanning](#security-scanning)
- [Django Extensions](#django-extensions)
- [Quick Commands](#quick-commands)
- [IDE Integration](#ide-integration)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Overview

This project uses multiple code quality tools to ensure consistent, clean, and secure code:

- **Ruff**: Fast Python linter (primary)
- **Flake8**: Additional style and quality checks
- **Pylint**: Comprehensive static analysis
- **Black**: Code formatter
- **isort**: Import sorter
- **mypy**: Static type checker
- **Bandit**: Security vulnerability scanner
- **django-extensions**: Development utilities

## Linting Tools

### Ruff (Primary Linter)

Fast, modern Python linter written in Rust. Replaces Flake8, isort, and more.

**Configuration**: `pyproject.toml`

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
```

**Run Ruff**:
```bash
# Check for issues
make lint

# Auto-fix issues
docker compose exec backend ruff check src/ --fix

# Check specific file
docker compose exec backend ruff check src/pets/models.py
```

**What Ruff Checks**:
- Code style (PEP 8)
- Unused imports and variables
- Code complexity
- Import order
- Bug-prone patterns
- Django-specific issues

### Flake8

Additional linting for catching edge cases.

**Configuration**: `.flake8`

```ini
[flake8]
max-line-length = 100
max-complexity = 10
```

**Run Flake8**:
```bash
# Via Makefile
docker compose exec backend flake8 src/

# Check specific app
docker compose exec backend flake8 src/pets/
```

### Pylint

Comprehensive static analysis with Django support.

**Configuration**: `pyproject.toml`

```toml
[tool.pylint.main]
load-plugins = ["pylint_django"]
django-settings-module = "config.settings.development"
```

**Run Pylint**:
```bash
# Check all apps
docker compose exec backend pylint src/*/

# Check specific app
docker compose exec backend pylint src/pets/

# Generate report
docker compose exec backend pylint src/*/ --output-format=text > pylint-report.txt
```

### Run All Linters

```bash
# Run all linters at once
make lint-all

# This runs: ruff, flake8, and pylint
```

## Code Formatting

### Black

Opinionated code formatter for consistent style.

**Configuration**: `pyproject.toml`

```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

**Format Code**:
```bash
# Format all code
make format

# Check formatting without changes
make format-check

# Format specific file
docker compose exec backend black src/pets/models.py
```

### isort

Import statement sorter.

**Configuration**: `pyproject.toml`

```toml
[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["config", "pets", "store", "users"]
```

**Sort Imports**:
```bash
# Sort all imports (included in 'make format')
docker compose exec backend isort src/

# Check import order
docker compose exec backend isort --check-only src/

# Sort specific file
docker compose exec backend isort src/pets/views.py
```

## Type Checking

### mypy

Static type checker with Django support.

**Configuration**: `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.12"
plugins = ["mypy_django_plugin.main", "mypy_drf_plugin.main"]
```

**Run Type Checks**:
```bash
# Check all code
make check

# Check specific file
docker compose exec backend mypy src/pets/models.py

# Generate report
docker compose exec backend mypy src/ --html-report mypy-report
```

**Type Hints Example**:
```python
from typing import Optional, List
from django.db.models import QuerySet

def get_available_pets(category_id: Optional[int] = None) -> QuerySet['Pet']:
    """Get available pets, optionally filtered by category."""
    queryset = Pet.objects.filter(status='available')
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    return queryset
```

## Security Scanning

### Bandit

Security vulnerability scanner.

**Configuration**: `pyproject.toml`

```toml
[tool.bandit]
exclude_dirs = ["/tests", "/migrations"]
skips = ["B101", "B601"]
```

**Run Security Scans**:
```bash
# Run security checks
make security

# Full scan with high and medium severity
docker compose exec backend bandit -r src/ -ll

# Generate JSON report
docker compose exec backend bandit -r src/ -f json -o bandit-report.json

# Check specific file
docker compose exec backend bandit src/users/views.py
```

**Common Security Issues Detected**:
- Hardcoded passwords
- SQL injection vulnerabilities
- Insecure cryptography
- Command injection
- Unsafe YAML loading

## Django Extensions

Powerful development utilities for Django.

### shell_plus

Enhanced Django shell with auto-imports.

```bash
# Open shell_plus
make shell-plus

# Or directly
docker compose exec backend python src/manage.py shell_plus
```

**Features**:
- Auto-imports all models
- IPython integration
- Syntax highlighting
- Tab completion

**Example Session**:
```python
# In shell_plus - models are already imported!
>>> Pet.objects.filter(status='available').count()
5

>>> user = User.objects.first()
>>> user.username
'admin'

>>> Category.objects.all()
<QuerySet [<Category: Dogs>, <Category: Cats>]>
```

### show_urls

Display all URL patterns in your project.

```bash
# Show all URLs
make show-urls

# Or directly
docker compose exec backend python src/manage.py show_urls
```

**Output Example**:
```
/admin/                              django.contrib.admin.site.urls
/api/docs/                           schema view
/v2/pet/                             pets-list
/v2/pet/<int:pk>/                    pets-detail
/v2/user/                            users-list
/v2/user/login/                      user-login
/v2/store/order/                     orders-list
...
```

### graph_models

Generate visual diagrams of your Django models.

**Prerequisites**: Requires `graphviz` installed in Docker container.

```bash
# Generate model diagram
make graph-models

# Output saved to: docs/diagrams/models.png
```

**Customize Output**:
```bash
# Generate for specific apps
docker compose exec backend python src/manage.py graph_models pets store -o pets-store.png

# Include fields
docker compose exec backend python src/manage.py graph_models -a -g -o full-diagram.png

# Output as DOT file
docker compose exec backend python src/manage.py graph_models -a -o models.dot
```

### Other Useful Commands

```bash
# Show database statistics
docker compose exec backend python src/manage.py sqlsequencereset pets

# Generate admin for models
docker compose exec backend python src/manage.py admin_generator pets

# Clear cache
docker compose exec backend python src/manage.py clear_cache

# Show model fields
docker compose exec backend python src/manage.py  describe_form pets.Pet
```

## Quick Commands

### Daily Development Workflow

```bash
# 1. Format code before committing
make format

# 2. Run quick lint check
make lint

# 3. Run tests
make test

# 4. Before PR: Run full quality checks
make quality
```

### Pre-Commit Checklist

```bash
# 1. Format code
make format

# 2. Check formatting
make format-check

# 3. Run all linters
make lint-all

# 4. Type checking
make check

# 5. Security scan
make security

# 6. Run tests with coverage
make test-cov

# Or run everything at once
make quality && make test-cov
```

### Fixing Issues

```bash
# Auto-fix linting issues
docker compose exec backend ruff check src/ --fix

# Format imports
docker compose exec backend isort src/

# Format code
docker compose exec backend black src/
```

## IDE Integration

### VSCode

**Recommended Extensions**:
- Python (Microsoft)
- Pylance
- Ruff
- Black Formatter
- isort
- mypy

**Settings** (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.banditEnabled": true,

  "python.formatting.provider": "black",
  "editor.formatOnSave": true,

  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },

  "isort.check": true,
  "mypy-type-checker.importStrategy": "fromEnvironment"
}
```

### PyCharm/IntelliJ IDEA

1. **Enable External Tools**:
   - Settings → Tools → External Tools
   - Add tools for: ruff, black, isort, mypy, bandit

2. **Configure File Watchers**:
   - Settings → Tools → File Watchers
   - Add watchers for automatic formatting

3. **Django Support**:
   - Enable Django support
   - Set Django settings module: `config.settings.development`

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run linters
        run: |
          ruff check src/
          flake8 src/
          pylint src/*/

      - name: Check formatting
        run: |
          black --check src/
          isort --check-only src/

      - name: Type checking
        run: mypy src/

      - name: Security scan
        run: bandit -r src/ -ll

      - name: Run tests
        run: pytest src/
```

### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs, djangorestframework-stubs]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
        args: [-ll, -r, src/]
```

Install hooks:
```bash
pip install pre-commit
pre-commit install
```

## Troubleshooting

### Linting Issues

**Problem**: "Module not found" errors in mypy

**Solution**:
```bash
# Ensure django-stubs is installed
docker compose exec backend pip install django-stubs djangorestframework-stubs

# Or rebuild with dev dependencies
docker compose exec backend pip install -e ".[dev]"
```

**Problem**: Ruff and Black conflicts

**Solution**: Black is configured to work with Ruff. Run format first:
```bash
make format
make lint
```

**Problem**: Pylint too strict for Django

**Solution**: Django-specific rules are disabled in `pyproject.toml`. Adjust as needed:
```toml
[tool.pylint.messages_control]
disable = ["E1101", "W0212"]  # Django dynamic attributes
```

### Django Extensions Issues

**Problem**: shell_plus not available

**Solution**:
```bash
# Ensure django-extensions is installed and in INSTALLED_APPS
docker compose exec backend python src/manage.py shell_plus
```

**Problem**: graph_models missing graphviz

**Solution**:
```bash
# Install graphviz in Dockerfile
RUN apt-get update && apt-get install -y graphviz
```

### Performance Issues

**Problem**: Linting is slow

**Solution**:
```bash
# Run linters in parallel (not in Makefile yet)
ruff check src/ & flake8 src/ & wait

# Or run only fast linters
make lint  # Just ruff (fast)
```

### False Positives

**Disable specific warnings**:

```python
# Disable for one line
result = eval(user_input)  # noqa: S307 (Bandit)

# Disable for block
# pylint: disable=no-member
user = User.objects.get(pk=1)
# pylint: enable=no-member

# Disable for file
# ruff: noqa: F401
from models import *  # Import all models
```

## Best Practices

1. **Run formatters before linters**: `make format` then `make lint`
2. **Use shell_plus for debugging**: More efficient than regular shell
3. **Check types early**: Catch errors before runtime
4. **Scan for security regularly**: Run `make security` before deploys
5. **Keep tools updated**: Update linter versions in `pyproject.toml`
6. **Fix issues incrementally**: Don't disable all warnings
7. **Use IDE integration**: Real-time feedback while coding
8. **Document exceptions**: When disabling warnings, add comments explaining why

## Additional Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Django Extensions Documentation](https://django-extensions.readthedocs.io/)

---

**Last Updated**: January 2026
