
import os
from collections.abc import AsyncIterator

import asyncpg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5435/hw",
)


async def get_db_connection() -> AsyncIterator[asyncpg.Connection]:
    """Открыть соединение с БД и закрыть его после запроса."""

    conn = await asyncpg.connect(DATABASE_URL)

    try:
        yield conn
    finally:
        await conn.close()

