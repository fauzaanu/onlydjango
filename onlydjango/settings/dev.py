"""Development settings."""

from os import path

from huey import PriorityRedisHuey

from .base import *
from .constants import dev as env

DEBUG = env.DEBUG
SECRET_KEY = env.SECRET_KEY
ALLOWED_HOSTS = env.ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = ["https://onlydjango.com", "https://www.onlydjango.com"]

# =============================================================================
# STORAGE
# =============================================================================
# Local storage for dev (set DEV_STORAGE=S3 in .env to use S3 instead)
if env.DEV_STORAGE != "S3":
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            "OPTIONS": {
                "location": path.join(BASE_DIR, "staticfiles"),
                "base_url": "/static/",
            },
        },
        "media": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": path.join(BASE_DIR, "media"),
                "base_url": "/media/",
            },
        },
    }

STATIC_URL = "static/"
STATIC_ROOT = path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    path.join(PROJECT_DIR, "static"),
]

# =============================================================================
# DATABASE
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.PGDATABASE,
        "USER": env.PGUSER,
        "PASSWORD": env.PGPASSWORD,
        "HOST": env.PGHOST,
        "PORT": env.PGPORT,
        "OPTIONS": {
            "pool": {
                "min_size": env.DB_POOL_MIN_SIZE,
                "max_size": env.DB_POOL_MAX_SIZE,
                "timeout": env.DB_POOL_TIMEOUT,
            }
        },
    }
}

# =============================================================================
# CACHE
# =============================================================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# =============================================================================
# HUEY (Background Tasks)
# =============================================================================
HUEY = PriorityRedisHuey(url=env.REDIS_URL)
HUEY.periodic_task_check_frequency = 1

# Flush Huey queue on startup (only if Redis is available)
try:
    HUEY.flush()
except Exception:
    pass  # Redis not running, skip flush

# =============================================================================
# LOGGING
# =============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "INFO",
        "handlers": ["console"],
        "propagate": "True",
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}
