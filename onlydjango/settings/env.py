"""
Centralized Environment Variable Access

All environment variables used in the project are defined here.
Import and use these variables in settings files via:

    from onlydjango.settings.env import VARIABLE_NAME
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Django Core
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
MAIN_HOST = os.getenv("MAIN_HOST", "onlydjango.com")
SITE_NAME = os.getenv("SITE_NAME")

# Database (PostgreSQL)
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
DB_POOL_MIN_SIZE = int(os.getenv("DB_POOL_MIN_SIZE", "5"))
DB_POOL_MAX_SIZE = int(os.getenv("DB_POOL_MAX_SIZE", "100"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "500"))

# Redis / Cache
REDIS_URL = os.getenv("REDIS_URL")
REDIS_PORT = os.getenv("REDIS_PORT")

# AWS S3 Storage
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")

# Telegram
TELEGRAM_BOT_ID = os.getenv("TELEGRAM_BOT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Email
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Development
DEV_STORAGE = os.getenv("DEV_STORAGE", "local")
