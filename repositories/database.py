
import os
from collections.abc import AsyncIterator

import asyncpg
from fastapi import HTTPException


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5435/hw",
)


async def get_db_connection() -> AsyncIterator[asyncpg.Connection]:
    """Открыть соединение с БД и закрыть его после запроса"""

    try:
        conn = await asyncpg.connect(DATABASE_URL)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed",
        ) from exc

    try:
        yield conn
    finally:
        await conn.close()
