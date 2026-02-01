from huey import PriorityRedisHuey

from .base import *
from .env import env
from onlydjango.helpers.host_utils import normalize_host

## HOST SETTINGS ##
# You should define `MAIN_HOST` as example.com in the ENV

DEBUG = False
MAIN_HOST = normalize_host(env.MAIN_HOST)
HTTPS_HOST = f"https://{MAIN_HOST}"
COOKIE_HOST = f".{MAIN_HOST}"

ALLOWED_HOSTS = [
    MAIN_HOST,
]

SECRET_KEY = env.DJANGO_SECRET_KEY
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
        "NAME": env.PGDATABASE,
        "USER": env.PGUSER,
        "PASSWORD": env.PGPASSWORD,
        "HOST": env.PGHOST,
        "PORT": env.PGPORT,
        "OPTIONS": {
            "pool": {
                'min_size': env.DB_POOL_MIN_SIZE,
                'max_size': env.DB_POOL_MAX_SIZE,
                'timeout': env.DB_POOL_TIMEOUT,
            }
        },
    }
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache

REDIS_URL = env.REDIS_URL
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
ADMINS = [("Admin", env.ADMIN_EMAIL)]

# Email settings
# https://docs.djangoproject.com/en/3.1/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.EMAIL_HOST_PASSWORD

# setup logging - log to file and email
# https://docs.djangoproject.com/en/5.0/topics/logging/

TELEGRAM_BOT_TOKEN = env.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = env.TELEGRAM_CHAT_ID

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
            "telegram_bot_token": TELEGRAM_BOT_TOKEN,
            "telegram_chat_id": TELEGRAM_CHAT_ID,
            "formatter": "telegram",
            "filters": ["exclude_disallowed_host"],
        },
        "error_handler": {
            "level": "ERROR",
            "class": "onlydjango.helpers.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": TELEGRAM_BOT_TOKEN,
            "telegram_chat_id": TELEGRAM_CHAT_ID,
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
