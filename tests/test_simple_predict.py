
import asyncio

import asyncpg
import pytest
from fastapi.testclient import TestClient

from main import app
from repositories.database import DATABASE_URL
from routers.predict import get_prediction_service


client = TestClient(app)


async def update_records(user_id, item_id, verified, images):
    """Изменить данные продавца и объявления перед тестом."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(
            "UPDATE users SET is_verified = $1 WHERE id = $2",
            verified,
            user_id,
        )
        await conn.execute(
            "UPDATE items SET images_qty = $1 WHERE id = $2",
            images,
            item_id,
        )
    finally:
        await conn.close()


@pytest.mark.parametrize(
    ("verified", "images", "expected"),
    [
        (True, 0, False),
        (True, 3, False),
        (False, 0, True),
        (False, 1, False),
        (False, 3, False),
    ],
)
def test_simple_predict(db_records, verified, images, expected):
    """Проверяем разные варианты предсказания."""
    asyncio.run(
        update_records(
            db_records["user_id"],
            db_records["item_id"],
            verified,
            images,
        )
    )

    response = client.post(
        "/simple_predict",
        params={"item_id": db_records["item_id"]},
    )

    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"item_id": "abc"},
        {"item_id": "1.5"},
        {"item_id": "-1"},
    ],
)
def test_invalid_item_id(params):
    """Проверяем неправильные входные значения."""
    response = client.post("/simple_predict", params=params)
    assert response.status_code == 400


def test_item_not_found():
    """Проверяем несуществующее объявление."""
    response = client.post(
        "/simple_predict",
        params={"item_id": 2147483647},
    )

    assert response.status_code == 404


def test_prediction_error_returns_500(db_records):
    """Проверяем ошибку внутри сервиса предсказания."""

    class BrokenService:
        def predict(self, request):
            raise RuntimeError("internal error")

    app.dependency_overrides[get_prediction_service] = (
        lambda: BrokenService()
    )

    try:
        response = client.post(
            "/simple_predict",
            params={"item_id": db_records["item_id"]},
        )
    finally:
        app.dependency_overrides.pop(
            get_prediction_service, None
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Prediction failed"}
