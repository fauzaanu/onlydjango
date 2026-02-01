"""Test settings optimized for speed.

Usage:
    uv run python manage.py test --settings=onlydjango.settings.tests --noinput

Or set in pyproject.toml:
    [tool.pytest.ini_options]
    DJANGO_SETTINGS_MODULE = "onlydjango.settings.tests"
"""

from .base import *

DEBUG = False
SECRET_KEY = "test-secret-key-not-for-production"

# =============================================================================
# DATABASE - SQLite in-memory for maximum speed
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# =============================================================================
# PASSWORD HASHER - Use fast hasher for tests
# =============================================================================
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# =============================================================================
# EMAIL - In-memory backend
# =============================================================================
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# =============================================================================
# CACHE - Local memory cache
# =============================================================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# =============================================================================
# STORAGE - In-memory file storage for tests
# =============================================================================
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# =============================================================================
# INSTALLED APPS - Remove debug toolbar for tests
# =============================================================================
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]

# =============================================================================
# MIDDLEWARE - Remove unnecessary middleware for tests
# =============================================================================
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# =============================================================================
# LOGGING - Disable logging during tests
# =============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}

# =============================================================================
# TEMPLATES - Disable debug for templates
# =============================================================================
for template in TEMPLATES:
    template["OPTIONS"]["debug"] = False

# =============================================================================
# CELERY/HUEY - Run tasks synchronously
# =============================================================================
HUEY = None  # Disable Huey in tests
