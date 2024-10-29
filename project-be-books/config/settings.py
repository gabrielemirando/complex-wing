import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Security

DEBUG = True
SECRET_KEY = "django-insecure-&@eu(#-6h8n+(jcqkrjk@#f2^8#&^s55+ux-p$t(=k77&@pt55"
ALLOWED_HOSTS = ["*"]

# Application definition

WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"

# Apps

INSTALLED_APPS = [
    "rest_framework",
    "app.config.Config",
    "drf_spectacular",
]

# Middlewares

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# REST framework

REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
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

# Cache

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
        "TIMEOUT": None,
    }
}

# Celery

RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "password")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", 5672)
RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "vhost")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}"
    f"@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
)
CELERY_TASK_IGNORE_RESULT = True

# API Docs

SPECTACULAR_SETTINGS = {
    "TITLE": "Book Service API",
    "DESCRIPTION": "API for posting reviews and ratings of books",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

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

# Testing overrides

IS_TEST = "test" in sys.argv or "test_coverage" in sys.argv

if IS_TEST:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DB_NAME", "bookdb"),
    }

    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }

    CELERY_BROKER_URL = "memory://"
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
