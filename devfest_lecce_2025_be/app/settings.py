import os
import logging
from pathlib import Path

from .utils import print_warning, print_section_start, print_section_end


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

ALLOWED_HOSTS = []


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
    # Custom apps
    "badges",
    "conferences",
    "speakers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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


#####################################################
# DATABASE
#####################################################

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
            "project_id": os.getenv("GS_PROJECT_ID"),
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
