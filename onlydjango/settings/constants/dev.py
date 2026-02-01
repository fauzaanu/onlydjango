"""Development environment constants.

All environment variables for local development are defined here.
This is the ONLY place where os.environ/os.getenv should be used.
"""

import os

# =============================================================================
# DATABASE
# =============================================================================
PGDATABASE = os.environ.get("PGDATABASE", "postgres")
PGUSER = os.environ.get("PGUSER", "postgres")
PGPASSWORD = os.environ.get("PGPASSWORD", "admin")
PGHOST = os.environ.get("PGHOST", "localhost")
PGPORT = os.environ.get("PGPORT", "5432")

# Database pool settings
DB_POOL_MIN_SIZE = 2
DB_POOL_MAX_SIZE = 4
DB_POOL_TIMEOUT = 10

# =============================================================================
# REDIS
# =============================================================================
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

# =============================================================================
# DJANGO CORE
# =============================================================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Dev Server
DEV_PORT = os.environ.get("DJANGO_DEV_PORT", "8000")

# =============================================================================
# STORAGE
# =============================================================================
DEV_STORAGE = os.environ.get("DEV_STORAGE", "local")

# AWS S3 (optional in dev)
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "")

# =============================================================================
# SITE INFO
# =============================================================================
SITE_NAME = os.environ.get("SITE_NAME", "onlydjango")
