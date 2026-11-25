
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



def test_missing_records(missing_ids):
    """Проверяем поиск отсутствующих записей"""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            users = UserRepository(conn)
            items = ItemRepository(conn)

            assert (
                await users.get_by_id(missing_ids["user_id"])
                is None
            )
            assert (
                await items.get_by_id(missing_ids["item_id"])
                is None
            )
            assert (
                await items.get_prediction_data(missing_ids["item_id"])
                is None
            )
        finally:
            await conn.close()

    asyncio.run(check())




def test_foreign_key(missing_ids):
    """Нельзя создать объявление для несуществующего продавца"""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            items = ItemRepository(conn)

            with pytest.raises(asyncpg.ForeignKeyViolationError):
                await items.create(
                    item_id=missing_ids["item_id"],
                    seller_id=missing_ids["user_id"],
                    name="Invalid seller",
                    description="Test",
                    category=1,
                    images_qty=1,
                )
        finally:
            await conn.close()

    asyncio.run(check())


def test_negative_images_rejected(db_records):
    """База запрещает отрицательное количество фотографий"""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            with pytest.raises(asyncpg.CheckViolationError):
                await conn.execute(
                    "UPDATE items SET images_qty = -1 WHERE id = $1",
                    db_records["item_id"],
                )
        finally:
            await conn.close()

    asyncio.run(check())


def test_negative_violations_rejected(db_records):
    """База запрещает отрицательное количество нарушений."""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            with pytest.raises(asyncpg.CheckViolationError):
                await conn.execute(
                    "UPDATE users SET violations_qty = -1 WHERE id = $1",
                    db_records["user_id"],
                )
        finally:
            await conn.close()

    asyncio.run(check())



def test_duplicate_user_id_rejected(db_records):
    """Нельзя создать двух пользователей с одинаковым ID."""

    async def check():
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            users = UserRepository(conn)

            with pytest.raises(asyncpg.UniqueViolationError):
                await users.create(
                    user_id=db_records["user_id"],
                    first_name="Another",
                    last_name="User",
                    is_verified=True,
                )
        finally:
            await conn.close()

    asyncio.run(check())


