from config import settings

from fastapi import APIRouter, status, Depends, Form
from fastapi.responses import JSONResponse

from .services.orm_services import revoke_active_tokens
from .dependencies import authorize_user, generate_access_token
from .shortcuts import get_json_response_with_bearer


router = APIRouter(
    prefix="/auth",
    tags=["Authorization Server"],
)


@router.post(settings.AUTH_URL)
async def login(data_object: dict[str, str] = Depends(authorize_user)) -> JSONResponse:
    """Аутентификация пользователя."""

    response: JSONResponse = get_json_response_with_bearer(data_object)

    response.set_cookie(
        key="refresh_token",
        value=data_object.get("refresh_token", ''),
        httponly=True,
        samesite="lax")

    return response


@router.post('/refresh-token')
async def get_new_access_token(new_access_token: dict[str, str] = Depends(generate_access_token)) -> JSONResponse:
    """Принимает токен обновления для выдачи нового токена доступа."""
    return get_json_response_with_bearer(new_access_token)


@router.post('/revoke-token')
async def revoke_token(token: str = Form(...)) -> JSONResponse:
    """Отзывает JWT токен."""
    revoked: bool = await revoke_active_tokens(token)            
    return JSONResponse(
            content={"Revoke token": "Токен был отозван!" if revoked else "Переданный токен уже отозван или выдан другим поставщиком!"}, 
            status_code=status.HTTP_200_OK if revoked else status.HTTP_400_BAD_REQUEST)