import logging
from os import path
from .base import *
from huey import RedisHuey

DEBUG = True
ALLOWED_HOSTS = [
    "*",
]
SECRET_KEY = "1234"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": path.join(BASE_DIR, "databases", "db.sqlite3"), # this is like this due to the
        # specific project having old data
    },
}

# Cache settings
# https://docs.djangoproject.com/en/5.0/topics/cache/#setting-up-the-cache
REDIS_URL = os.environ["REDIS_URL"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Tasks backend
HUEY = RedisHuey(url=REDIS_URL)


TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # When a message is given to the logger, the log level of the message is compared to the log level
    # of the logger. If
    # the log level of the message meets or exceeds the log level of the logger itself, the message will undergo
    # further processing. If it doesn’t, the message will be ignored. Once a logger has determined that a message
    # needs to be processed, it is passed to a Handler.
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
            "class": "onlydjango.telegram_logging.TelegramBotHandler",
            "telegram_bot_token": TELEGRAM_BOT_TOKEN,
            "telegram_chat_id": TELEGRAM_CHAT_ID,
        },
    },

}

