from typing import Literal, Any

from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from database.models import User

from .services.jwt_services import issuing_tokens, jwt_decode
from .services.auth_services import authenticate_user, check_revoking_token
from .services.orm_services import commit_tokens_user, get_current_user, update_access_token

from .shortcuts import get_instance_unauthorized_exception


async def authorize_user(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[Literal['access_token', 'refresh_token'], str]:
    """Зависимость для авторизации пользователей."""

    user: User | None = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise get_instance_unauthorized_exception()

    access_token, refresh_token = issuing_tokens(user)
    await commit_tokens_user(user, access_token=access_token, refresh_token=refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


async def generate_access_token(refresh_token: str = Form(...)) -> dict[Literal['access_token'], str]:
    """Зависимость по генерации нового токена доступа."""

    payload: dict[str, Any] = jwt_decode(refresh_token)

    await check_revoking_token(refresh_token)

    user: User = await get_current_user(username=payload.get("sub", ''))
    access_token, _ = issuing_tokens(user)

    await update_access_token(refresh_token, access_token)

    return {"access_token": access_token}