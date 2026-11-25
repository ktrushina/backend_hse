import asyncio
import uuid

import asyncpg
import pytest

from repositories.database import DATABASE_URL
from repositories.items import ItemRepository
from repositories.users import UserRepository


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def db_records():
    """Создаём тестовые записи и удаляем их после теста"""

    user_id = uuid.uuid4().int % 1_000_000_000 + 100_000_000
    item_id = uuid.uuid4().int % 1_000_000_000 + 100_000_000

    async def setup():
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            users = UserRepository(conn)
            items = ItemRepository(conn)

            await users.create(
                user_id=user_id,
                first_name="Test",
                last_name="Seller",
                is_verified=False,
                violations_qty=0,
            )

            await items.create(
                item_id=item_id,
                seller_id=user_id,
                name="Test item",
                description="Test description",
                category=1,
                images_qty=0,
            )
        finally:
            await conn.close()

    async def cleanup():
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            await conn.execute(
                "DELETE FROM items WHERE id = $1",
                item_id,
            )
            await conn.execute(
                "DELETE FROM users WHERE id = $1",
                user_id,
            )
        finally:
            await conn.close()

    run(setup())

    try:
        yield {"user_id": user_id, "item_id": item_id}
    finally:
        run(cleanup())


@pytest.fixture
def missing_ids():
    """Подобрать ID, которых точно нет в обеих таблицах"""

    async def find_missing_ids():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            while True:
                candidate = uuid.uuid4().int % 2_000_000_000 + 1

                user_exists = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)",
                    candidate,
                )

                item_exists = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM items WHERE id = $1)",
                    candidate,
                )

                if not user_exists and not item_exists:
                    return {
                        "user_id": candidate,
                        "item_id": candidate,
                    }
        finally:
            await conn.close()

    return asyncio.run(find_missing_ids())

