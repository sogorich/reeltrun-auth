from config import settings
from typing import Generator, Any

from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta 

from database.models import User
from auth.shortcuts import get_instance_unauthorized_exception


def generate_user_claims(username: str, expires: timedelta) -> dict[str, Any]:
    """Генерирует клэймы для токена пользователя."""
    return {
        "sub": username,
        "exp": datetime.utcnow() + expires
    }


def jwt_encode(claims: dict[str, Any]) -> str:
    """Кодирует информацию в jwt-токен и возвращает его."""
    return jwt.encode(key=settings.SECRET_KEY, algorithm=settings.BASE_HASH_ALGORITHM, claims=claims)


def jwt_decode(token: str | bytes) -> dict[str, Any]:
    """Декодирует информацию из jwt-токена и возвращает словарь с клэймами."""    
    try:
        return jwt.decode(key=settings.SECRET_KEY, algorithms=settings.BASE_HASH_ALGORITHM, token=token)

    except ExpiredSignatureError:
        raise get_instance_unauthorized_exception(
            message="Время жизни токена истекло!")

    except JWTError:
        raise get_instance_unauthorized_exception(
            message="Передан невалидный токен!")


def issuing_tokens(user: User) -> Generator[str, None, None]:
    """Выдача токенов пользователю."""
    return (
        jwt_encode(
            generate_user_claims(user.username, token_exp))
        for token_exp in (settings.ACCESS_TOKEN_LIFETIME, settings.REFRESH_TOKEN_LIFETIME)
    )