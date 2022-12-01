from config import settings, crons

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from auth import endpoints as auth_router
from client import endpoints as client_router

from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import ValidationError

from config.exceptions_handlers import validation_error_exception_handler
from config.middleware import logging_middleware


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESC,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
    license_info=settings.APP_LICENSE,
    terms_of_service=settings.APP_TERMS,
    contact=settings.APP_CONTACTS)

app.include_router(auth_router.router)
app.include_router(client_router.router)

app.add_exception_handler(ValidationError, validation_error_exception_handler)

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(CORSMiddleware, 
                    allow_origins=settings.CORS_ORIGINS,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

register_tortoise(app,
        generate_schemas=True,
        add_exception_handlers=True,
        config=settings.TORTOISE_ORM_CONFIG
    )

crons.CronMonitor()