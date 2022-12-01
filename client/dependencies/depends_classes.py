from typing import Any
from fastapi import Form, Depends

from auth.services.auth_services import verify_access_token


class UserData:
    """Определяет базовые данные пользователя для объекта FormData."""

    def __init__(
        self, 
        first_name: str | None = Form(default=None, description="Имя"),
        second_name: str | None = Form(default=None, description="Фамилия"),
        phone: str | None = Form(default=None, description="Номер телефона")
    ) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.phone = phone

    def serialize_to_dict(self) -> dict[str, Any]:
        """Возвращает словарь с данными, определёнными в конструкторе."""
        return self.__dict__


class UserAccessToken:
    """Определяет зависимость на токен доступа пользователя."""

    def __init__(self, access_token: dict[str, Any] = Depends(verify_access_token)) -> None:
        self._access_token = access_token

    @property
    def get_subject(self) -> str:
        """Возвращает предмет токена (клэйм sub)."""
        return self._access_token.get('sub', '')