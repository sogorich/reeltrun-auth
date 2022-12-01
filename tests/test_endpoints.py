import pytest, httpx

from asgi_lifespan import LifespanManager
from fastapi import status

from server import app


@pytest.fixture(scope="module")
def anyio_backend():
    """Текущий механизм тестирования."""
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    """Прокидывает асинхронного клиента в asgi приложении через события startup/shutdown."""
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
            yield ac


@pytest.mark.anyio
async def test_get_client_credentials_without_authorize(client: httpx.AsyncClient):
    """Тест на получение клиентских данных без авторизации."""
    response = await client.get('/users/profile')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_user(client: httpx.AsyncClient):
    """Тестим создание пользователя."""
    data = {
        'username': 'testuser',
        'password': '123456',
        'email': 'testuser@mail.ru',
    }  
    response = await client.post("/users/create", data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.anyio
async def test_login_user(client: httpx.AsyncClient):
    """Тестим успешную авторизацию пользователя."""
    data = {
        'username': 'testuser',
        'password': '123456',
    }
    response = await client.post("/auth/login", data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_login_user_fail(client: httpx.AsyncClient):
    """Тестим провальную авторизацию пользователя."""
    data = {
        'username': 'testuser',
        'password': '654321',
    }
    response = await client.post("/auth/login", data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_new_access_token_fail(client: httpx.AsyncClient):
    """Тестим получение токена доступа, если передан невалидный токен обновления."""
    data = {
        "refresh_token": "fake_refresh_token"
    }
    response = await client.post('/auth/refresh-token', data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_revoke_token_fail(client: httpx.AsyncClient):
    """Тестим отзыв токена в том случае, когда он был выдан другим поставщиком."""
    data = {
        "token": "faketoken"
    }
    response = await client.post('/auth/revoke-token', data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
