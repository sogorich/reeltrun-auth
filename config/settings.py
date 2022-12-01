import os, sys, pathlib

from typing import Type

from loguru import logger
from dotenv import load_dotenv

from datetime import timedelta
from fastapi import exceptions


# Enviroment 
DEBUG_MODE: bool = True
load_dotenv('dev.env' if DEBUG_MODE else 'prod.env')

# Base options
APP_TITLE = "ReelTrun"
APP_DESC = "Сервис аутентификации и авторизации"
APP_TERMS = "Использование в соответствии с лицензией MIT"

APP_VERSION = "0.1"
APP_LICENSE = {
    "name": "MIT License",
    "url": "https://github.com/sogorich/reeltrun-auth/blob/master/LICENSE",
}
APP_CONTACTS = {
    "name": "Egor Tchyorniy",
    "email": "so.gorich@inbox.ru",
}

# CORS
CORS_ORIGINS = os.environ['CORS_ORIGINS'].split()

# OpenAPI
OPENAPI_URL = os.environ['OPENAPI_URL']
REDOC_URL = os.environ['REDOC_URL']
DOCS_URL = os.environ['DOCS_URL']

# Crypto
SECRET_KEY = os.environ['SECRET_KEY']
BASE_HASH_ALGORITHM = os.environ['BASE_HASH_ALGORITHM']

# Auth options
AUTH_URL: str = "/login"
AUTH_TOKEN_URL: str = "/auth" + AUTH_URL

ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=float(os.environ['ACCESS_TOKEN_LIFETIME']))
REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=float(os.environ['REFRESH_TOKEN_LIFETIME']))

# Databases options
TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": os.environ['DATABASE_DSN'],
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# App options
BASIC_EXCEPTIONS: tuple[Type[Exception], ...] = (
    exceptions.RequestValidationError,
    exceptions.WebSocketRequestValidationError,
    exceptions.HTTPException)

# Logging
logger_config = {
    "handlers": [
        {
            "sink": pathlib.Path("logs/logs.log"),
            "enqueue": True,
            "format": "{time} | {level} | {name}:{function}:{line} - {message}", 
            "compression": "zip", 
            "rotation": "10 KB",
        },
        {
            "sink": sys.stdout,
            "enqueue": True,
        }
    ]
}
logger.configure(**logger_config)