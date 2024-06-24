from .base import *
from huey import RedisHuey

DEBUG = False
ALLOWED_HOSTS = [
    "localhost",
    "beta.lessonfuse.com",
    "lessonfuse.com",
    "staging.lessonfuse.com"
]
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # secret

CSRF_TRUSTED_ORIGINS = [
    "https://lessonfuse.com",
    "https://beta.lessonfuse.com",
]
CSRF_COOKIE_DOMAIN = ".lessonfuse.com"
SESSION_COOKIE_DOMAIN = ".lessonfuse.com"
CSRF_COOKIE_SECURE = True

# for django all auth
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "databases", "db.sqlite3"),
#     },
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["PGDATABASE"],
        "USER": os.environ["PGUSER"],
        "PASSWORD": os.environ["PGPASSWORD"],
        "HOST": os.environ["PGHOST"],
        "PORT": os.environ["PGPORT"],
    }
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache

REDIS_URL = "redis://redis:6379"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            REDIS_URL,  # primary
        ],
        "KEY_PREFIX": "lessonfuse",
    }
}

# Email to receive error logs
ADMINS = [("Fauzaan", "hello@fauzaanu.com")]

# Email settings
# https://docs.djangoproject.com/en/3.1/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]  # secrets
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]  # secrets

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
            "class": "onlydjango.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": os.environ["TELEGRAM_BOT_TOKEN"],
            "telegram_chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "formatter": "telegram",
            "filters": ["exclude_disallowed_host"],
        },
        "error_handler": {
            "level": "ERROR",
            "class": "onlydjango.telegram_logging.TelegramBotHandler",
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

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
HUEY = RedisHuey("huey", host=REDIS_HOST, port=REDIS_PORT)


