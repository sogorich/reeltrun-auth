from __future__ import annotations

from typing import Type
from datetime import datetime

from database.models import ActiveJWTToken
from tortoise.expressions import Q

import aiocron


class CronMonitor:
    """Управляет периодическими задачами."""

    def __new__(cls: Type[CronMonitor]) -> Type[CronMonitor]:
        return cls

    @aiocron.crontab("0 3 * * *")
    async def _remove_expired_tokens() -> None:
        """Удаляет все просроченные сессии токенов."""

        current_datetime: datetime = datetime.utcnow()
        await ActiveJWTToken.filter(Q(expired__lt=current_datetime) | Q(expired=None)).delete()

        print("[!] Произведена очистка просроченных токенов")