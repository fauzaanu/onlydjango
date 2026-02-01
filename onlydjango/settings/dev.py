from os import path
from .base import *
from . import env
from huey import PriorityRedisHuey

DEBUG = True
CSRF_TRUSTED_ORIGINS = ["https://onlydjango.com", "https://www.onlydjango.com"]
ALLOWED_HOSTS = [
    "*",
]
SECRET_KEY = "1234"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Use any S3 Compatible storage backend for static and media files
# AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_S3_SIGNATURE_VERSION = "s3v4"
# AWS_S3_CUSTOM_DOMAIN = "cdn.onlydjango.com"
os.environ.setdefault('DEV_STORAGE', 'local')  # use `S3` for S3

if env.DEV_STORAGE == "local":
    # No Else needed as base contains S3 settings configured
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            "OPTIONS": {
                "location": path.join(BASE_DIR, "staticfiles"),  # noqa
                "base_url": "/static/",
            },
        },

        "media": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": path.join(BASE_DIR, "media"),  # noqa
                "base_url": "/media/",
            },
        },
    }

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # noqa
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),  # noqa
]

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
                "min_size": 2,
                "max_size": 4,
                "timeout": 10,
            }
        },
    }
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache
REDIS_URL = env.REDIS_URL
REDIS_PORT = env.REDIS_PORT
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


HUEY = PriorityRedisHuey(host='localhost', port=REDIS_PORT)
HUEY.flush()
# sometimes huey refuses to start tasks
HUEY.periodic_task_check_frequency = 1

TELEGRAM_BOT_TOKEN = env.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = env.TELEGRAM_CHAT_ID
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "INFO",
        "handlers": ["console"],
        "propagate": "True",
    },
    "loggers": {
        "telegram_logger": {
            "handlers": ["telegram"],
            "level": "ERROR",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "telegram": {
            "level": "DEBUG",
            "class": "onlydjango.helpers.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": TELEGRAM_BOT_TOKEN,
            "telegram_chat_id": TELEGRAM_CHAT_ID,
        },
    },

}
