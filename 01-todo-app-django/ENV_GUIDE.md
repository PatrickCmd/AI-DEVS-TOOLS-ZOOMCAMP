# Environment Variables Guide

## Overview

This guide explains all environment variables used in the Django TODO application and how to configure them for different environments.

## Quick Start

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   nano .env  # or vim, code, etc.
   ```

3. **Restart services if already running:**
   ```bash
   make restart
   # or: docker compose restart
   ```

## Environment Files

### `.env`
- Actual configuration (gitignored)
- Contains sensitive data
- **NEVER commit to version control**

### `.env.example`
- Template with defaults
- Safe to commit
- Documents all available variables

## Required Variables

### Database Configuration

#### `POSTGRES_DB`
- **Description:** PostgreSQL database name
- **Default:** `todo_db`
- **Example:** `POSTGRES_DB=my_todo_database`
- **Used by:** Database container and Django

#### `POSTGRES_USER`
- **Description:** PostgreSQL username
- **Default:** `todo_user`
- **Example:** `POSTGRES_USER=admin`
- **Used by:** Database container and Django

#### `POSTGRES_PASSWORD`
- **Description:** PostgreSQL password
- **Default:** `todo_password`
- **Security:** Change in production!
- **Generate strong password:**
  ```bash
  openssl rand -base64 32
  ```
- **Example:** `POSTGRES_PASSWORD=Xy9$mK2!pQ7@vN4#zR8`

#### `POSTGRES_HOST`
- **Description:** Database host address
- **Default:** `db` (Docker service name)
- **Docker:** Use `db`
- **Local:** Use `localhost` or `127.0.0.1`
- **Remote:** Use IP or hostname

#### `POSTGRES_PORT`
- **Description:** PostgreSQL port
- **Default:** `5432`
- **Note:** Rarely needs changing

### Django Configuration

#### `DJANGO_SECRET_KEY`
- **Description:** Secret key for cryptographic signing
- **Default:** `django-insecure-change-this-in-production`
- **Security:** **MUST** change in production!
- **Generate:**
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- **Online generator:** https://djecrety.ir/
- **Length:** 50+ characters recommended
- **Example:** `DJANGO_SECRET_KEY=t5$9#mX@k2!pQ7&vN4*zR8^wL3%yH6`

#### `DEBUG`
- **Description:** Enable/disable debug mode
- **Default:** `True`
- **Development:** `True`
- **Production:** `False`
- **Security:** **NEVER** use `True` in production!
- **Impact:**
  - Shows detailed error pages
  - Exposes settings in errors
  - Disables security features

## Optional Variables

### Django Advanced

#### `ALLOWED_HOSTS`
- **Description:** Comma-separated list of allowed host/domain names
- **Default:** `*` (allows all - development only)
- **Development:** `*` or `localhost,127.0.0.1`
- **Production:** `your-domain.com,www.your-domain.com`
- **Example:** `ALLOWED_HOSTS=example.com,www.example.com,api.example.com`

#### `TIMEZONE`
- **Description:** Application timezone
- **Default:** `UTC`
- **Options:** [TZ database names](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- **Examples:**
  - `TIMEZONE=UTC`
  - `TIMEZONE=America/New_York`
  - `TIMEZONE=Europe/London`
  - `TIMEZONE=Asia/Tokyo`

#### `LANGUAGE_CODE`
- **Description:** Default language
- **Default:** `en-us`
- **Examples:**
  - `LANGUAGE_CODE=en-us`
  - `LANGUAGE_CODE=es`
  - `LANGUAGE_CODE=fr`
  - `LANGUAGE_CODE=de`

### Email Configuration

#### `EMAIL_BACKEND`
- **Description:** Email backend to use
- **Development:** `django.core.mail.backends.console.EmailBackend`
- **Production:** `django.core.mail.backends.smtp.EmailBackend`

#### `EMAIL_HOST`
- **Description:** SMTP server hostname
- **Gmail:** `smtp.gmail.com`
- **SendGrid:** `smtp.sendgrid.net`
- **Mailgun:** `smtp.mailgun.org`

#### `EMAIL_PORT`
- **Description:** SMTP port
- **TLS:** `587`
- **SSL:** `465`

#### `EMAIL_USE_TLS`
- **Description:** Use TLS encryption
- **Default:** `True`

#### `EMAIL_HOST_USER`
- **Description:** SMTP username
- **Example:** `your-email@gmail.com`

#### `EMAIL_HOST_PASSWORD`
- **Description:** SMTP password
- **Gmail:** Use App Password, not account password

### Static/Media Files

#### `STATIC_ROOT`
- **Description:** Directory for collected static files
- **Example:** `STATIC_ROOT=/var/www/static/`
- **When needed:** Production deployment

#### `MEDIA_ROOT`
- **Description:** Directory for user uploads
- **Example:** `MEDIA_ROOT=/var/www/media/`

### Security (Production)

#### `SECURE_SSL_REDIRECT`
- **Description:** Redirect HTTP to HTTPS
- **Production:** `True`
- **Development:** `False`

#### `SESSION_COOKIE_SECURE`
- **Description:** Send session cookie over HTTPS only
- **Production:** `True`

#### `CSRF_COOKIE_SECURE`
- **Description:** Send CSRF cookie over HTTPS only
- **Production:** `True`

### External Services

#### `REDIS_URL`
- **Description:** Redis connection URL
- **Example:** `redis://redis:6379/0`
- **Use cases:** Caching, sessions, Celery

#### `SENTRY_DSN`
- **Description:** Sentry error tracking DSN
- **Example:** `https://abc123@sentry.io/123456`

## Environment-Specific Configurations

### Development `.env`
```bash
# Database
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=dev_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=dev-secret-key-not-for-production
DEBUG=True
```

### Production `.env`
```bash
# Database
POSTGRES_DB=todo_production
POSTGRES_USER=todo_prod_user
POSTGRES_PASSWORD=Xy9$mK2!pQ7@vN4#zR8^wL3%yH6  # Strong password!
POSTGRES_HOST=db.production.internal
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=t5$9#mX@k2!pQ7&vN4*zR8^wL3%yH6$jB9  # Generated secret!
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Testing `.env`
```bash
# Database
POSTGRES_DB=todo_test
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=test-secret-key
DEBUG=True
```

## Security Best Practices

### 1. Never Commit `.env`
```bash
# .gitignore should contain:
.env
```

### 2. Use Strong Secrets

**Secret Key:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Passwords:**
```bash
openssl rand -base64 32
```

### 3. Rotate Secrets Regularly
- Change passwords every 90 days
- Rotate secret keys after security incidents
- Update API keys when compromised

### 4. Use Different Values Per Environment
- Development secrets ≠ Production secrets
- Different databases per environment
- Separate API keys for dev/prod

### 5. Secure Storage in Production
- Use environment variables (not files)
- Use secret management services:
  - AWS Secrets Manager
  - HashiCorp Vault
  - Google Secret Manager
  - Azure Key Vault

## Loading Environment Variables

### Docker Compose
Automatically loads `.env` file:
```yaml
# docker-compose.yml
services:
  web:
    env_file:
      - .env
```

### Django Settings
Uses `python-dotenv`:
```python
# settings.py
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### Shell Export (Manual)
```bash
export POSTGRES_DB=todo_db
export DJANGO_SECRET_KEY=your-secret-key
```

## Troubleshooting

### Variables Not Loading
```bash
# Check if .env exists
ls -la .env

# Verify format (no quotes needed)
cat .env

# Restart containers
make restart
```

### Connection Refused
```bash
# Check database host
# Docker: use 'db'
# Local: use 'localhost'

# Verify database is running
make ps
docker compose ps db
```

### Secret Key Error
```bash
# Generate new secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Add to .env
echo "DJANGO_SECRET_KEY=<generated-key>" >> .env
```

### Debug Mode Issues
```bash
# Check current value
docker compose run --rm web uv run python -c "from django.conf import settings; print(settings.DEBUG)"

# Fix in .env
DEBUG=True  # Development
DEBUG=False  # Production
```

## Validation

### Check Environment Variables
```bash
# View all variables
docker compose config

# Check specific service
docker compose run --rm web env | grep POSTGRES

# Verify Django settings
make shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.DATABASES)
```

### Test Database Connection
```bash
make dbshell
# If connected, environment is correct
```

## Migration Guide

### From Development to Production

1. **Copy `.env.example`:**
   ```bash
   cp .env.example .env.production
   ```

2. **Update critical values:**
   - Generate new `DJANGO_SECRET_KEY`
   - Set strong `POSTGRES_PASSWORD`
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`

3. **Enable security features:**
   ```bash
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

4. **Test before deploying:**
   ```bash
   docker compose --env-file .env.production config
   ```

## Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/ref/settings/)
- [PostgreSQL Environment Variables](https://www.postgresql.org/docs/current/libpq-envars.html)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [12-Factor App Configuration](https://12factor.net/config)

## Support

For issues with environment configuration:
1. Check this guide
2. Verify `.env.example` for correct format
3. Review [README.md](README.md) for setup instructions
4. Run `make check` to verify Django configuration
