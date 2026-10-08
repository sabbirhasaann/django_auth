import os
from .base import *

DEBUG = os.environ.get('DEBUG_DEV') == 'True'

SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS_DEV').split(",")


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE_DEV'),
        'NAME': os.environ.get('DB_NAME_DEV'),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get('DB_ENGINE_DEV'),
#         "HOST": os.environ.get("DB_HOST_DEV"),
#         "NAME": os.environ.get("DB_NAME_DEV"),
#         "USER": os.environ.get("DB_USER_DEV"),
#         "PASSWORD": os.environ.get("DB_PASS_DEV"),
#         "PORT": os.environ.get("DB_PORT_DEV", "5432"),
#         "OPTIONS": {
#             "sslmode": "require",
#         },
#     }
# }


MAILERS = {
    'default': {
        'BACKEND': os.environ.get("DB_MAILERS_BACKEND"),
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    'EXCEPTION_HANDLER': 'config.utils.custom_exception_handler',
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "TaskFlow API",
    "DESCRIPTION": "API for managing projects, tasks, comments, and attachments.",
    "VERSION": "1.0.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
