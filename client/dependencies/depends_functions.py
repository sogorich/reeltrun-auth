from fastapi import Form, Depends, HTTPException, status
from database.models import User

from auth.services.crypt_services import compute_hash, verify_hash, password_updating_hash
from auth.services.orm_services import get_current_user

from .depends_classes import UserData, UserAccessToken


async def create_new_user(
    username: str = Form(..., description="Логин"),
    email: str = Form(..., description="Электронная почта"),
    password: str = Form(..., description="Пароль"),
    form_data_of_user: UserData = Depends()
) -> User:
    """Зависимость, которая создаёт нового пользователя в базе данных."""

    user_obj: User = await User.create(
        password=compute_hash(password), 
        username=username, 
        email=email,
        **form_data_of_user.serialize_to_dict())

    return user_obj


async def update_client_credentials(
        access_token: UserAccessToken = Depends(),
        form_data_of_user: UserData = Depends()
    ) -> User:
    """Зависимость, выполняющая обновление пользовательских данных."""

    await User.filter(username=access_token.get_subject).update(**form_data_of_user.serialize_to_dict())
    return await get_current_user(username=access_token.get_subject)


async def changing_the_user_password(
        access_token: UserAccessToken = Depends(),
        old_password: str = Form(..., description="Текущий пароль"), 
        new_password: str = Form(..., description="Новый пароль")
    ) -> None:
    """Зависимость для изменения пароля у пользователя."""

    if old_password == new_password:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Введёные пароли не должны быть одинаковыми!")

    user: User = await get_current_user(username=access_token.get_subject)
    hashed_valid, _ = verify_hash(old_password, user.password)

    if not hashed_valid:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Прошлый пароль от аккаунта неверный!")
    
    await password_updating_hash(user.pk, compute_hash(new_password))


async def delete_account_user(access_token: UserAccessToken = Depends()) -> None:
    """Зависимость по удалению пользователя."""
    user: User = await get_current_user(username=access_token.get_subject) 
    await user.delete() 


async def get_data_of_user(access_token: UserAccessToken = Depends()) -> User:
    """Получает всю информацию об аккаунте через токен доступа."""
    return await get_current_user(username=access_token.get_subject)