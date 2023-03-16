from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-37cf#7qc08t*z@ojq=on=9kv7s_=ase1x6$_@^a3mgx+s#l_p+"

INSTALLED_APPS += ["drf_yasg"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOW_ALL_ORIGINS = True
