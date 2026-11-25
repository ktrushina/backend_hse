
import asyncpg


class ItemRepository:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def create(
        self,
        item_id: int,
        seller_id: int,
        name: str,
        description: str,
        category: int,
        images_qty: int,
    ) -> int:
        """Добавить объявление в БД."""
        return await self.conn.fetchval(
            """
            INSERT INTO items (
                id, seller_id, name, description,
                category, images_qty
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            """,
            item_id,
            seller_id,
            name,
            description,
            category,
            images_qty,
        )

    async def get_by_id(self, item_id: int):
        """Получить объявление по ID."""
        return await self.conn.fetchrow(
            "SELECT * FROM items WHERE id = $1",
            item_id,
        )

    async def get_prediction_data(self, item_id: int):
        """Получить объявление и продавца одним SQL-запросом."""
        return await self.conn.fetchrow(
            """
            SELECT
                i.id AS item_id,
                i.seller_id,
                i.name,
                i.description,
                i.category,
                i.images_qty,
                u.is_verified AS is_verified_seller
            FROM items AS i
            INNER JOIN users AS u
                ON i.seller_id = u.id
            WHERE i.id = $1
            """,
            item_id,
        )
