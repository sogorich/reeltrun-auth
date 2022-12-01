from tortoise import BaseDBAsyncClient # type:ignore


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(64) NOT NULL UNIQUE /* Логин */,
    "email" VARCHAR(128) NOT NULL UNIQUE /* Электронная почта */,
    "password" VARCHAR(128) NOT NULL  /* Пароль */,
    "first_name" VARCHAR(64)   /* Имя */,
    "second_name" VARCHAR(64)   /* Фамилия */,
    "phone" VARCHAR(64)   /* Номер телефона */,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Создан */
) /* Модель пользователя. */;
CREATE TABLE IF NOT EXISTS "activejwttoken" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "access_token" VARCHAR(384) NOT NULL  /* Токен доступа */,
    "refresh_token" VARCHAR(384) NOT NULL  /* Токен обновления */,
    "expired" TIMESTAMP   /* Действует до */,
    "owner_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
) /* Модель активных JWT токенов (access and refresh tokens). */;
CREATE INDEX IF NOT EXISTS "idx_activejwtto_access__3084d8" ON "activejwttoken" ("access_token");
CREATE INDEX IF NOT EXISTS "idx_activejwtto_refresh_9b54d7" ON "activejwttoken" ("refresh_token");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
