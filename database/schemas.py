from datetime import datetime
from .models import UserOut


class UserOutProxy(UserOut):
    """Проксирует поля pydantic—модели пользователя для поддержки типизации."""

    id: int

    username: str
    email: str

    first_name: str | None
    second_name: str | None
    phone: str | None

    created: datetime