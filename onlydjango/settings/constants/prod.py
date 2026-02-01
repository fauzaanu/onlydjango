"""Production environment constants.

All environment variables for production are defined here.
This is the ONLY place where os.environ/os.getenv should be used.
"""

import os

# =============================================================================
# DATABASE (Railway private network)
# =============================================================================
PGDATABASE = os.environ["PGDATABASE"]
PGUSER = os.environ["PGUSER"]
PGPASSWORD = os.environ["PGPASSWORD"]
PGHOST = os.environ["PGHOST"]
PGPORT = os.environ["PGPORT"]

# Database pool settings
DB_POOL_MIN_SIZE = int(os.environ.get("DB_POOL_MIN_SIZE", "5"))
DB_POOL_MAX_SIZE = int(os.environ.get("DB_POOL_MAX_SIZE", "100"))
DB_POOL_TIMEOUT = int(os.environ.get("DB_POOL_TIMEOUT", "500"))

# =============================================================================
# REDIS (Railway private network)
# =============================================================================
REDIS_URL = os.environ["REDIS_URL"]

# =============================================================================
# DJANGO CORE
# =============================================================================
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
MAIN_HOST = os.environ.get("MAIN_HOST", "onlydjango.com")

# Server
PORT = os.environ.get("PORT", "8000")

# =============================================================================
# STORAGE (AWS S3 - required in prod)
# =============================================================================
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_ENDPOINT_URL = os.environ["AWS_S3_ENDPOINT_URL"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN", "")

# =============================================================================
# EMAIL
# =============================================================================
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

# =============================================================================
# SITE INFO
# =============================================================================
SITE_NAME = os.environ.get("SITE_NAME", "onlydjango")
