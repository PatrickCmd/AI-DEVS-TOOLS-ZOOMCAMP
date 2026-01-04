# Multi-stage Dockerfile for Petstore API

# Stage 1: Base image with uv
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Stage 2: Development image
FROM base as development

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Create src directory for package installation
RUN mkdir -p src && touch src/__init__.py

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Copy application code
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p logs media staticfiles

# Expose port
EXPOSE 8000

# Run development server
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

# Stage 3: Production image
FROM base as production

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Create src directory for package installation
RUN mkdir -p src && touch src/__init__.py

# Install production dependencies only
RUN uv pip install --system .

# Copy application code
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p logs media staticfiles

# Collect static files
RUN python src/manage.py collectstatic --noinput --clear || true

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60", "config.wsgi:application"]
