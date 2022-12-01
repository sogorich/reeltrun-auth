from typing import Dict

from tortoise.contrib.pydantic.base import PydanticModel

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from database.schemas import UserOutProxy
from database.models import User

from .dependencies.depends_functions import (
                            create_new_user,  
                            update_client_credentials,
                            changing_the_user_password,
                            delete_account_user,
                            get_data_of_user)


router = APIRouter(
    prefix='/users',
    tags=['Resource Server']
)


@router.post('/create', response_model=UserOutProxy, status_code=status.HTTP_201_CREATED)
async def create_user(created_user: User = Depends(create_new_user)) -> PydanticModel:
    """Создание нового пользователя."""
    return await UserOutProxy.from_tortoise_orm(created_user)


@router.get('/profile', response_model=UserOutProxy)
async def get_user_profile(user_profile: User = Depends(get_data_of_user)) -> PydanticModel:
    """Профиль пользователя (возвращет все данные аккаунта)."""
    return await UserOutProxy.from_tortoise_orm(user_profile)


@router.put('/update', response_model=UserOutProxy)
async def update_user(updated_user: User = Depends(update_client_credentials)) -> PydanticModel:
    """Обновление пользовательских данных."""
    return await UserOutProxy.from_tortoise_orm(updated_user)


@router.put('/password/change', response_model=Dict[str, str], dependencies=[Depends(changing_the_user_password)])
async def change_password() -> JSONResponse:
    """Изменение пароля у пользователя."""
    return JSONResponse(content={"changed": "Пароль был успешно изменён!"})


@router.delete('/delete', dependencies=[Depends(delete_account_user)])
async def delete_account() -> JSONResponse:
    """Удаление пользовательского аккаунта."""
    return JSONResponse(content={"deleted": "Аккаунт был успешно удалён!"})