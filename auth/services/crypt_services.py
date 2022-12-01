from passlib.context import CryptContext
from database.models import User


crypt_context = CryptContext(schemes=['bcrypt_sha256'], deprecated="auto")


def compute_hash(raw_data: str) -> str:
    """Вычисление хеша по сырым данным."""
    return crypt_context.hash(raw_data)


def verify_hash(raw_data: str, hashed_data: str) -> tuple[bool, str | None]:
    """
        Проверка сырых данных на соответствие хешированным. 
        Также проверяет хэш на актуальность, в случае просрочки вычисляет новую хеш-сумму.
    """
    return crypt_context.verify_and_update(raw_data, hashed_data)


async def password_updating_hash(user_id: int, new_hashed_password: str) -> int:
    """Перезаписывает хеш пароля у пользователя."""
    return await User.filter(id=user_id).update(password=new_hashed_password)