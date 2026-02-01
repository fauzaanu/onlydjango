"""Base settings shared between dev and prod."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

# Import constants based on environment
_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "onlydjango.settings.dev")
if "prod" in _settings_module:
    from .constants import prod as env
else:
    from .constants import dev as env

PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent
WSGI_APPLICATION = "onlydjango.wsgi.application"

# =============================================================================
# INSTALLED APPS
# =============================================================================
FIRST_PARTY_APPS = [
    "onlydjango",
    "apps.core",
]

ALL_AUTH_APPS = [
    "allauth",
    "allauth.account",
]

THIRD_PARTY_APPS = [
    "django_browser_reload",
    "huey.contrib.djhuey",
    "django_cotton",
    "debug_toolbar",
    "django_extensions",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
]

INSTALLED_APPS = DJANGO_APPS + ALL_AUTH_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS

# =============================================================================
# MIDDLEWARE
# =============================================================================
SITE_ID = 1
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "onlydjango.urls"

# =============================================================================
# TEMPLATES
# =============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "onlydjango.helpers.onlydjango_globals.global_settings",
            ],
        },
    },
]

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Indian/Maldives"
USE_I18N = False
USE_TZ = True

# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# ALLAUTH
# =============================================================================
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================
AUTH_USER_MODEL = "core.User"

# =============================================================================
# AWS S3 STORAGE (from constants)
# =============================================================================
AWS_STORAGE_BUCKET_NAME = env.AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = env.AWS_S3_ENDPOINT_URL
AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 3600
AWS_S3_CUSTOM_DOMAIN = env.AWS_S3_CUSTOM_DOMAIN

STORAGES = {
    "default": {
        "BACKEND": "onlydjango.storage.private.PrivateMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "custom_domain": env.AWS_S3_CUSTOM_DOMAIN,
        },
    },
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [PROJECT_DIR / "static"]

# =============================================================================
# SITE INFO (from constants)
# =============================================================================
SITE_VERSION = "0.0.1"
SITE_NAME = env.SITE_NAME
SITE_AUTHOR = ""
SITE_KEYWORDS = ""
SITE_DESCRIPTION = ""
OG_TYPE = ""
OG_TITLE = ""
OG_DESCRIPTION = ""
OG_IMAGE = ""
TWITTER_CARD = ""
TWITTER_TITLE = ""
TWITTER_DESCRIPTION = ""
TWITTER_IMAGE = ""
