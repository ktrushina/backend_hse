
import asyncpg


class UserRepository:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def create(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        is_verified: bool,
        violations_qty: int = 0,
    ) -> int:
        """Добавить пользователя в БД."""
        return await self.conn.fetchval(
            """
            INSERT INTO users (
                id, first_name, last_name,
                is_verified, violations_qty
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            user_id,
            first_name,
            last_name,
            is_verified,
            violations_qty,
        )

    async def get_by_id(self, user_id: int):
        """Получить пользователя по его ID."""
        return await self.conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            user_id,
        )
