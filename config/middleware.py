from config import settings

from fastapi import Request, status
from fastapi.responses import JSONResponse

from typing import Any, Callable
from loguru import logger


async def logging_middleware(request: Request, call_next: Callable[[Request], Any]):
    """Промежуточное ПО, которое обрабатывает все неотловленные ошибки и сохраняет их в логи."""
    
    try:
        response = await call_next(request)
 
    except settings.BASIC_EXCEPTIONS:
        raise

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e} | Endpoint: {request.scope['path']} ({request.scope['endpoint'].__name__})")
        await logger.complete()

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Произошла ошибка. Разработчики уже получили сообщение об этой ситуации и проблема в скором времени будет исправлена."
            })

    return response