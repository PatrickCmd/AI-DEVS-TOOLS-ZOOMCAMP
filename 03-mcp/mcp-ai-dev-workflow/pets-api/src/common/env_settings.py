"""
Pydantic settings for environment configuration.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the base directory (project root, not src)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class EnvironmentSettings(BaseSettings):
    """
    Application environment settings loaded from environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Literal["development", "production", "test"] = Field(
        default="development", description="Application environment"
    )

    # Django Core
    secret_key: str = Field(
        default="django-insecure-change-me-in-production",
        description="Django secret key for cryptographic signing",
    )
    debug: bool = Field(default=True, description="Enable debug mode")
    allowed_hosts: str = Field(
        default="localhost,127.0.0.1,0.0.0.0,backend",
        description="Comma-separated list of allowed hosts",
    )

    def get_allowed_hosts_list(self) -> list[str]:
        """Convert allowed_hosts string to list."""
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    # Database
    database_url: str = Field(
        default="postgresql://petstore:petstore@localhost:5432/petstore_db",
        description="PostgreSQL database URL",
    )

    def get_database_config(self) -> dict:
        """Parse database URL and return Django database configuration."""
        from urllib.parse import urlparse

        parsed = urlparse(self.database_url)
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/") if parsed.path else "petstore_db",
            "USER": parsed.username or "petstore",
            "PASSWORD": parsed.password or "petstore",
            "HOST": parsed.hostname or "localhost",
            "PORT": parsed.port or 5432,
            "CONN_MAX_AGE": 600,
        }

    # API Settings
    api_key_header: str = Field(
        default="api_key", description="Header name for API key authentication"
    )
    default_api_key: str = Field(
        default="special-key", description="Default API key for testing"
    )

    # OAuth2 Settings
    oauth2_authorization_url: str = Field(
        default="http://petstore.swagger.io/oauth/dialog",
        description="OAuth2 authorization URL",
    )

    # CORS
    cors_allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000",
        description="Comma-separated list of CORS allowed origins",
    )

    def get_cors_allowed_origins_list(self) -> list[str]:
        """Convert cors_allowed_origins string to list."""
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    # Static and Media
    static_url: str = Field(default="/static/", description="Static files URL")
    media_url: str = Field(default="/media/", description="Media files URL")
    media_root: str = Field(default="media", description="Media files root directory")

    # Pagination
    page_size: int = Field(default=20, description="Default pagination page size")
    max_page_size: int = Field(default=100, description="Maximum pagination page size")


# Global instance
env_settings = EnvironmentSettings()
