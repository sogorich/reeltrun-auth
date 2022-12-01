from tortoise import models, fields
from tortoise.contrib.pydantic.creator import pydantic_model_creator
 
from .validators import EmailValidator


class ActiveJWTToken(models.Model):
    """Модель активных JWT токенов (access and refresh tokens)."""

    access_token = fields.CharField(max_length=384, index=True, description="Токен доступа")
    refresh_token = fields.CharField(max_length=384, index=True, description="Токен обновления")
    expired = fields.DatetimeField(description="Действует до", null=True)
    owner = fields.ForeignKeyField("models.User", related_name="active_tokens") 

    def __str__(self) -> str:
        return f'Токены принадлежат {self.owner}'

    class Meta:
        db_table = "active_jwt_tokens"


class User(models.Model):
    """Модель пользователя."""

    username = fields.CharField(
        max_length=64, description="Логин", unique=True)
    email = fields.CharField(
        max_length=128, description="Электронная почта", unique=True, validators=[EmailValidator()])
    password = fields.CharField(max_length=128, description="Пароль")

    first_name = fields.CharField(max_length=64, description="Имя", null=True)
    second_name = fields.CharField(
        max_length=64, description="Фамилия", null=True)
    phone = fields.CharField(
        max_length=64, description="Номер телефона", null=True)

    created = fields.DatetimeField(auto_now_add=True, description="Создан")

    active_tokens: fields.BackwardFKRelation[ActiveJWTToken]

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = "user"


UserOut = pydantic_model_creator(User, name='PydanticUserOut', exclude=('password',))