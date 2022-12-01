from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def get_instance_unauthorized_exception(
        message: str = "Вы ввели некорректные данные!", 
        include_header: bool = True) -> HTTPException:
    """Возвращает класс исключения, возбуждающий 401 ошибку."""

    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"} if include_header else {}
    )


def get_json_response_with_bearer(data: dict[str, str]) -> JSONResponse:
    """Формирует JSON ответ с предъявителем."""
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={**data, "token_type": "Bearer"}
    )