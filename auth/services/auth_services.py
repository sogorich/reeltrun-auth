from config import settings

from typing import Any
from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from database.models import User, ActiveJWTToken
from auth.shortcuts import get_instance_unauthorized_exception

from .crypt_services import verify_hash, password_updating_hash
from .orm_services import get_active_tokens

from . import jwt_services


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.AUTH_TOKEN_URL)


async def authenticate_user(username: str, password: str) -> None | User:
    """Аутентификация пользователя."""

    user: User | None = await User.get_or_none(username=username)

    if not user:
        return None

    hash_valid, new_hash = verify_hash(password, user.password)

    if not hash_valid:
        return None

    if new_hash:
        await password_updating_hash(user.pk, new_hash)

    return user


async def check_revoking_token(token: str) -> None:
    """Проверяет токен на предмет отзыва."""
    token_is_active: ActiveJWTToken | None = await get_active_tokens(token)

    if not token_is_active:
        raise get_instance_unauthorized_exception(
            message="Указанный Вами токен был отозван!")

    return None


async def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """Верификация токена. Позволяет узнать, был ли токен доступа скомпрометирован."""

    token_decoded: dict[str, Any] = jwt_services.jwt_decode(token)

    await check_revoking_token(token)
    
    return token_decoded