from .base import *

DEBUG = True

INSTALLED_APPS += ["drf_spectacular"]

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': 'PinIt API',
    'DESCRIPTION': 'API for the PinIt web app',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOW_ALL_ORIGINS = True
