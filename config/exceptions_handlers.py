from fastapi import Request, status
from fastapi.responses import JSONResponse

from tortoise.exceptions import ValidationError


async def validation_error_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Перехватывает все ошибки возникаемые от ValidationError и транслирует их на клиент в виде json."""
    return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            content={"validation_error": f"{exc}"})