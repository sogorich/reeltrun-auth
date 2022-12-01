from config import settings
from typing import Literal, Any

from datetime import datetime
from fastapi import status, HTTPException

from database.models import User, ActiveJWTToken
from tortoise.expressions import Q
    

async def get_current_user(**user_data: Any) -> User:
    """Возвращет текущего пользователя."""
    return await User.get(**user_data)


async def commit_tokens_user(current_user: User, **tokens: Any) -> None:
    """Фиксирует токены пользователя в базе как активные."""

    acceptable_keys: frozenset[Literal['access_token', 'refresh_token']] = frozenset(('access_token', 'refresh_token'))

    for key in tokens.keys():
        if key not in acceptable_keys:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Недопустимые данные!")

    tokens_expired: datetime = datetime.utcnow() + settings.REFRESH_TOKEN_LIFETIME
    await ActiveJWTToken.create(owner=current_user, expired=tokens_expired, **tokens)


async def update_access_token(refresh_token: str, new_access_token: str) -> int:
    """Выдаёт новый токен доступа по токену обновления."""

    refresh_token_in_stock: bool = await ActiveJWTToken.exists(refresh_token=refresh_token)

    if not refresh_token_in_stock:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, 
            detail="Токен был отозван или Вы передаёте не токен обновления!")

    return await ActiveJWTToken.filter(refresh_token=refresh_token).update(access_token=new_access_token)


async def get_active_tokens(token: str) -> ActiveJWTToken | None:
    """Получение пары активных токенов (access_token / refresh_token)."""
    return await ActiveJWTToken.get_or_none(
        Q(Q(access_token=token) | Q(refresh_token=token))
    )


async def revoke_active_tokens(token: str) -> bool:
    """Находит пару активных токенов по переданному токену и отзывает их."""
    active_tokens: ActiveJWTToken | None = await get_active_tokens(token)

    if active_tokens:
        await active_tokens.delete(); return True

    return False