<img src="https://user-images.githubusercontent.com/48412168/205148407-7649497b-0a21-4b9e-80ef-8f64b80cf70b.svg" width="400" />

🛡 Сервис аутентификации и авторизации. 

Система основана на протоколе OAuth2.0 с реализацией потока паролей (password flow), 
обеспечивающие взаимодействие с клиентскими службами через Json Web Tokens (JWT).

**Ключевые моменты системы**

1. Создание аккаунта;
2. Аутентификация и авторизация;
3. Изменение персональных данных аккаунта;
4. Изменение пароля от аккаунта;
5. Удаление аккаунта;
6. Механизм формирования, верификации и принудительного отзыва токенов;
7. Фиксация активных сессий пользователя;
8. Крон-задачи, для удаления просроченных зафиксированных сессий. (по умолчанию удаление происходит каждый день в 03:00 по UTC);
9. Организация логирования приложения, в том числе предотвращение внештатных ситуаций, возникающих при необработанных серверных ошибках.

## Начало работы
Перед началом использования сервиса необходимо применить миграции и установить зависимости.

**Выполните следующие команды:**
<pre>
pip install -r ./requirements.txt
</pre>
<pre>
aerich init -t database.option.TORTOISE_ORM
</pre>
<pre>
aerich init-db
</pre>
<pre>
aerich migrate
</pre>
<pre>
aerich upgrade
</pre>
**Если нужно сбросить миграции:**
<pre>
Удалите базу данных и директорию с миграциями
</pre>
<pre>
aerich init-db
</pre>

**Создайте файлы dev.env и prod.env со следующим содержимым**
<pre>
# OpenAPI
OPENAPI_URL="/openapi.json"
REDOC_URL="/redoc"
DOCS_URL="/docs"

# JWT
ACCESS_TOKEN_LIFETIME=15 # in minutes
REFRESH_TOKEN_LIFETIME=21 # in days

# Crypto
SECRET_KEY="ВАШ_СЕКРЕТНЫЙ_КЛЮЧ"
BASE_HASH_ALGORITHM="HS256"

# Database
DATABASE_DSN="sqlite://db.sqlite3"

# CORS
CORS_ORIGINS="http://127.0.0.1 http://127.0.0.1:8000"
</pre>

***dev.env** используется в дебаг-режиме.

**Для Postgres установить следующий DSN в переменную DATABASE_DSN:**
<pre>
DATABASE_DSN="postgres://user:pass@localhost:5432/postgres"
</pre>

**Запуск приложения**

В самостоятельном режиме:
<pre>
uvicorn server:app --reload
</pre>

В качестве sub-application:
<pre>
app.mount("/path", auth_app)
</pre>
- **app**: Экземпляр Вашего приложения FastAPI;
- **auth_app**: Экземпляр сервиса авторизации.

## Технологический стек проекта
- Фреймворк FastAPI
- Object Relation Mapping Tortoise ORM
- Миграции Aerich
- Логирование Loguru
- Кроны aiocron
- Тесты pytest

## Перспективы. Дальнейшее развитие.
Планируется организовать этот сервис как поставщика авторизации (identity provider), 
с поддержкой SSO и соответствия со спецификацией Open ID Connect — что, возможно, 
будет реализовано как отдельно изолированное FastAPI приложение.


![Group 6](https://user-images.githubusercontent.com/48412168/205160358-6f924cba-21db-42e4-aabf-f469ce6a572d.png)
