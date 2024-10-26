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
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "app.config.Config",
]

# REST framework

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

# Database

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bookdb",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
