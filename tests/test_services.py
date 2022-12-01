import pytest

from fastapi import status, HTTPException

from database.models import User
from auth.services.orm_services import commit_tokens_user


@pytest.mark.anyio
async def test_commit_tokens_user():
    """Тест сервиса по фиксации токенов на предмет передачи недопустимых ключей."""
    
    fake_user: User = User()

    try:
        await commit_tokens_user(fake_user, id_token="faketoken", access_token="faketoken2")

    except HTTPException as e:
        assert e.status_code == status.HTTP_406_NOT_ACCEPTABLE