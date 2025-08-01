import os

from huey import PriorityRedisHuey

from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    "onlydjango.com",
]
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # secret

CSRF_TRUSTED_ORIGINS = [
    "https://onlydjango.com",
    "https://beta.onlydjango.com",
    "https://staging.onlydjango.com",
]
CSRF_COOKIE_DOMAIN = ".onlydjango.com"
SESSION_COOKIE_DOMAIN = ".onlydjango.com"
CSRF_COOKIE_SECURE = True


# Use any S3 Compatible storage backend for static and media files
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 3600

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "default_acl": "private",
        },
    },
    "media": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "default_acl": "private",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "custom_domain": os.getenv("AWS_S3_CUSTOM_DOMAIN"),
        },
    },
}


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"), #noqa
]


# for django all auth
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
            REDIS_URL,  # primary
        ],
        "KEY_PREFIX": SITE_NAME, #noqa
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

HUEY = PriorityRedisHuey('huey', url=REDIS_URL)
# sometimes huey refuses to start tasks
HUEY.periodic_task_check_frequency = 1


