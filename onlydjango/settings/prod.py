"""Production settings."""

from huey import PriorityRedisHuey

from .base import *
from .constants import prod as env
from onlydjango.helpers.host_utils import normalize_host

# =============================================================================
# HOST SETTINGS
# =============================================================================
DEBUG = env.DEBUG
MAIN_HOST = normalize_host(env.MAIN_HOST)
HTTPS_HOST = f"https://{MAIN_HOST}"
COOKIE_HOST = f".{MAIN_HOST}"

ALLOWED_HOSTS = [MAIN_HOST]
SECRET_KEY = env.SECRET_KEY

CSRF_TRUSTED_ORIGINS = [HTTPS_HOST]
CSRF_COOKIE_DOMAIN = COOKIE_HOST
SESSION_COOKIE_DOMAIN = COOKIE_HOST
CSRF_COOKIE_SECURE = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

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
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [env.REDIS_URL],
        "KEY_PREFIX": env.SITE_NAME,
    }
}

# =============================================================================
# EMAIL
# =============================================================================
ADMINS = [("Admin", env.ADMIN_EMAIL)]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.EMAIL_HOST_PASSWORD

# =============================================================================
# LOGGING
# =============================================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {
        "handlers": ["mail_admins", "console"],
        "level": "INFO",
        "propagate": True,
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# =============================================================================
# HUEY (Background Tasks)
# =============================================================================
HUEY = PriorityRedisHuey("huey", url=env.REDIS_URL)
HUEY.periodic_task_check_frequency = 1
