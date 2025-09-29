import os

from huey import PriorityRedisHuey

from .base import *
from onlydjango.helpers.host_utils import normalize_host

## HOST SETTINGS ##
# You should define `MAIN_HOST` as example.com in the ENV

DEBUG = False
MAIN_HOST = normalize_host(os.getenv('MAIN_HOST', 'onlydjango.com'))
HTTPS_HOST = f"https://{MAIN_HOST}"
COOKIE_HOST = f".{MAIN_HOST}"

ALLOWED_HOSTS = [
    MAIN_HOST,
]

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
CSRF_TRUSTED_ORIGINS = [
    HTTPS_HOST,
]

CSRF_COOKIE_DOMAIN = COOKIE_HOST
SESSION_COOKIE_DOMAIN = COOKIE_HOST
CSRF_COOKIE_SECURE = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# POSTGRES
# noinspection DuplicatedCode
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["PGDATABASE"],
        "USER": os.environ["PGUSER"],
        "PASSWORD": os.environ["PGPASSWORD"],
        "HOST": os.environ["PGHOST"],
        "PORT": os.environ["PGPORT"],
        "OPTIONS": {
            "pool": {
                'min_size': int(os.getenv('DB_POOL_MIN_SIZE', 5)),
                'max_size': int(os.getenv('DB_POOL_MAX_SIZE', 100)),
                'timeout': int(os.getenv('DB_POOL_TIMEOUT', 500)),
            }
        },
    }
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache

REDIS_URL = os.environ["REDIS_URL"]
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            REDIS_URL,
        ],
        "KEY_PREFIX": SITE_NAME,  # noqa
    }
}

# Email to receive error logs
ADMINS = [("Admin", os.environ["ADMIN_EMAIL"])]

# Email settings
# https://docs.djangoproject.com/en/3.1/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

# setup logging - log to file and email
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "telegram": {
            "level": "INFO",
            "class": "onlydjango.helpers.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": os.environ["TELEGRAM_BOT_TOKEN"],
            "telegram_chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "formatter": "telegram",
            "filters": ["exclude_disallowed_host"],
        },
        "error_handler": {
            "level": "ERROR",
            "class": "onlydjango.helpers.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": os.environ["TELEGRAM_BOT_TOKEN"],
            "telegram_chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "formatter": "telegram",
            "filters": ["exclude_disallowed_host"],
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "formatters": {
        "telegram": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    "root": {
        "handlers": ["error_handler", "console"],
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
    "filters": {
        "exclude_disallowed_host": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: not record.name.startswith("django.security.DisallowedHost"),
        },
    },
}

HUEY = PriorityRedisHuey('huey', url=REDIS_URL)
HUEY.periodic_task_check_frequency = 1
