from .base import *
from decouple import config
from datetime import timedelta

DEBUG = True

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test-database",
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


# AWS S3
S3_PINS_BUCKET_NAME = "pinit-staging"
S3_PINS_BUCKET_URL = "pinit-staging.s3.eu-west-3.amazonaws.com"
