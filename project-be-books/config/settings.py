import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security

DEBUG = True
SECRET_KEY = "django-insecure-&@eu(#-6h8n+(jcqkrjk@#f2^8#&^s55+ux-p$t(=k77&@pt55"
ALLOWED_HOSTS = ["*"]

# Application definition

WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"
STATIC_URL = "static/"

# Apps

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "rest_framework",
    "app.config.Config",
]

# Django middlewares

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# REST framework

REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "bookdb"),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Celery configuration

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# Django templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]
