
import asyncio

import asyncpg
import pytest

from repositories.database import DATABASE_URL
from repositories.items import ItemRepository
from repositories.users import UserRepository


def test_create_and_read_records(db_records):
    """Проверяем созданные фикстурой записи в обеих таблицах."""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            users = UserRepository(conn)
            items = ItemRepository(conn)

            user = await users.get_by_id(db_records["user_id"])
            item = await items.get_by_id(db_records["item_id"])
            joined = await items.get_prediction_data(
                db_records["item_id"]
            )

            assert user["first_name"] == "Test"
            assert user["is_verified"] is False
            assert user["violations_qty"] == 0

            assert item["seller_id"] == db_records["user_id"]
            assert item["images_qty"] == 0

            assert joined["seller_id"] == db_records["user_id"]
            assert joined["is_verified_seller"] is False
            assert joined["item_id"] == db_records["item_id"]
        finally:
            await conn.close()

    asyncio.run(check())


def test_missing_records():
    """Проверяем поиск несуществующих записей."""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            users = UserRepository(conn)
            items = ItemRepository(conn)

            assert await users.get_by_id(2147483647) is None
            assert await items.get_by_id(2147483647) is None
            assert await items.get_prediction_data(2147483647) is None
        finally:
            await conn.close()

    asyncio.run(check())


def test_foreign_key(db_records):
    """Нельзя создать объявление с несуществующим продавцом."""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            items = ItemRepository(conn)

            with pytest.raises(asyncpg.ForeignKeyViolationError):
                await items.create(
                    item_id=2147483646,
                    seller_id=2147483647,
                    name="Invalid seller",
                    description="Test",
                    category=1,
                    images_qty=1,
                )
        finally:
            await conn.close()

    asyncio.run(check())
