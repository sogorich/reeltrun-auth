from typing import Any

from tortoise.validators import Validator
from tortoise.exceptions import ValidationError

from email_validator import EmailNotValidError, validate_email


class EmailValidator(Validator):
    """Обёртка над валидацией email для поля модели."""

    def __call__(self, value: Any):
        try:
            validate_email(email=value)

        except EmailNotValidError:
            raise ValidationError("Передан невалидный email")