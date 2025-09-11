import logging
import os
from pathlib import Path

from .utils import print_section_end, print_section_start, print_warning

logging.basicConfig(level=logging.DEBUG)


BASE_DIR = Path(__file__).resolve().parent.parent


print_section_start("Settings Initialization")


#####################################################
# SECURITY
#####################################################

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "django-insecure-z&-aca$_@z_!p7)@7ii#gt!$#v3$i#+o$ap^t&3)-7#bsebw32"
    print_warning(
        "SECRET_KEY is not set. Using a default value, which is insecure for production!"
    )

DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
if DEBUG:
    print_warning("DEBUG is set to True. This should only be used in development!")

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
)
if "*" in ALLOWED_HOSTS:
    print_warning(
        "ALLOWED_HOSTS contains '*'. This is insecure and should not be used in production!"
    )

_CORS_ALLOWED_ORIGINS = (
    os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if os.getenv("CORS_ALLOWED_ORIGINS")
    else []
)
if "*" in _CORS_ALLOWED_ORIGINS:
    print_warning(
        "CORS_ALLOWED_ORIGINS contains '*'. This is insecure and should not be used in production!"
    )
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = _CORS_ALLOWED_ORIGINS

CSRF_TRUSTED_ORIGINS = (
    os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if os.getenv("CSRF_TRUSTED_ORIGINS")
    else []
)


#####################################################
# APPLICATION
#####################################################

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "import_export",
    "drf_yasg",
    "corsheaders",
    # Custom apps
    "badges",
    "conferences",
    "connections",
    "leaderboard",
    "rooms",
    "speakers",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "app.authentication.FirebaseAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "scan": "20/minute",
    },
}


#####################################################
# DATABASE
#####################################################

if os.getenv("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }
else:
    print_warning(
        "POSTGRES_URL is not set. Using SQLite for development. This is not recommended for production!"
    )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#####################################################
# AUTHENTICATION
#####################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


#####################################################
# INTERNATIONALIZATION
#####################################################

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


#####################################################
# STORAGE
#####################################################

if os.getenv("GS_BUCKET_NAME") is not None:
    _GOOGLE_CLOUD_STORAGE = {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": os.getenv("GS_BUCKET_NAME"),
            "querystring_auth": False,
        },
    }

    STORAGES = {
        "default": _GOOGLE_CLOUD_STORAGE,
        "staticfiles": _GOOGLE_CLOUD_STORAGE,
    }

else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    print_warning(
        "Google Cloud Storage is not configured. Using local file storage instead."
    )

STATIC_URL = "static/"

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"


print_section_end("Settings Initialization")
