"""
Centralized Environment Variable Access

All environment variables used in the project should be accessed through this file.
This provides a single source of truth for environment configuration and makes it
easy to see all required environment variables at a glance.

Usage:
    from onlydjango.settings.env import env

    # In settings files:
    SECRET_KEY = env.DJANGO_SECRET_KEY
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)


def _get_env(key: str, default: str | None = None, required: bool = False) -> str | None:
    """
    Get an environment variable with optional default and required validation.

    Args:
        key: The environment variable name
        default: Default value if not set (ignored if required=True)
        required: If True, raises an error when the variable is not set

    Returns:
        The environment variable value or default
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def _get_env_int(key: str, default: int) -> int:
    """Get an environment variable as an integer with a default value."""
    value = os.environ.get(key)
    if value is None:
        return default
    return int(value)


class EnvConfig:
    """
    Centralized environment variable access.

    All environment variables are accessed as properties, making it clear
    what variables are used and providing type hints.
    """

    # ===================
    # Django Core
    # ===================

    @property
    def DJANGO_SECRET_KEY(self) -> str | None:
        """Django secret key for cryptographic signing."""
        return _get_env("DJANGO_SECRET_KEY")

    @property
    def MAIN_HOST(self) -> str:
        """Main hostname for the application."""
        return _get_env("MAIN_HOST", default="onlydjango.com")  # type: ignore

    @property
    def SITE_NAME(self) -> str | None:
        """Site name used for branding and cache key prefix."""
        return _get_env("SITE_NAME")

    # ===================
    # Database (PostgreSQL)
    # ===================

    @property
    def PGDATABASE(self) -> str | None:
        """PostgreSQL database name."""
        return _get_env("PGDATABASE")

    @property
    def PGUSER(self) -> str | None:
        """PostgreSQL username."""
        return _get_env("PGUSER")

    @property
    def PGPASSWORD(self) -> str | None:
        """PostgreSQL password."""
        return _get_env("PGPASSWORD")

    @property
    def PGHOST(self) -> str | None:
        """PostgreSQL host address."""
        return _get_env("PGHOST")

    @property
    def PGPORT(self) -> str | None:
        """PostgreSQL port number."""
        return _get_env("PGPORT")

    @property
    def DB_POOL_MIN_SIZE(self) -> int:
        """Database connection pool minimum size."""
        return _get_env_int("DB_POOL_MIN_SIZE", default=5)

    @property
    def DB_POOL_MAX_SIZE(self) -> int:
        """Database connection pool maximum size."""
        return _get_env_int("DB_POOL_MAX_SIZE", default=100)

    @property
    def DB_POOL_TIMEOUT(self) -> int:
        """Database connection pool timeout in seconds."""
        return _get_env_int("DB_POOL_TIMEOUT", default=500)

    # ===================
    # Redis / Cache
    # ===================

    @property
    def REDIS_URL(self) -> str | None:
        """Redis connection URL."""
        return _get_env("REDIS_URL")

    @property
    def REDIS_PORT(self) -> str | None:
        """Redis port number (for local development)."""
        return _get_env("REDIS_PORT")

    # ===================
    # AWS S3 Storage
    # ===================

    @property
    def AWS_STORAGE_BUCKET_NAME(self) -> str | None:
        """AWS S3 bucket name for file storage."""
        return _get_env("AWS_STORAGE_BUCKET_NAME")

    @property
    def AWS_S3_ENDPOINT_URL(self) -> str | None:
        """AWS S3 endpoint URL (for S3-compatible services)."""
        return _get_env("AWS_S3_ENDPOINT_URL")

    @property
    def AWS_ACCESS_KEY_ID(self) -> str | None:
        """AWS access key ID."""
        return _get_env("AWS_ACCESS_KEY_ID")

    @property
    def AWS_SECRET_ACCESS_KEY(self) -> str | None:
        """AWS secret access key."""
        return _get_env("AWS_SECRET_ACCESS_KEY")

    @property
    def AWS_S3_CUSTOM_DOMAIN(self) -> str | None:
        """Custom domain for AWS S3 (CDN domain)."""
        return _get_env("AWS_S3_CUSTOM_DOMAIN")

    # ===================
    # Telegram
    # ===================

    @property
    def TELEGRAM_BOT_ID(self) -> str | None:
        """Telegram bot ID for social auth."""
        return _get_env("TELEGRAM_BOT_ID")

    @property
    def TELEGRAM_BOT_TOKEN(self) -> str | None:
        """Telegram bot token for API access and logging."""
        return _get_env("TELEGRAM_BOT_TOKEN")

    @property
    def TELEGRAM_CHAT_ID(self) -> str | None:
        """Telegram chat ID for error logging."""
        return _get_env("TELEGRAM_CHAT_ID")

    # ===================
    # Email
    # ===================

    @property
    def ADMIN_EMAIL(self) -> str | None:
        """Admin email address for error notifications."""
        return _get_env("ADMIN_EMAIL")

    @property
    def EMAIL_HOST_USER(self) -> str | None:
        """SMTP email host username."""
        return _get_env("EMAIL_HOST_USER")

    @property
    def EMAIL_HOST_PASSWORD(self) -> str | None:
        """SMTP email host password."""
        return _get_env("EMAIL_HOST_PASSWORD")

    # ===================
    # Development
    # ===================

    @property
    def DEV_STORAGE(self) -> str:
        """Development storage backend ('local' or 'S3')."""
        return _get_env("DEV_STORAGE", default="local")  # type: ignore


# Singleton instance for importing
env = EnvConfig()
