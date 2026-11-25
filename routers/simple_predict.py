import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query

from repositories.database import get_db_connection
from repositories.items import ItemRepository
from routers.predict import get_prediction_service
from schemas.predict import PredictionRequest
from services.predict import PredictionService


router = APIRouter()



@router.post(
    "/simple_predict",
    response_model=bool,
    responses={
        400: {
            "description": "Некорректный идентификатор объявления",
        },
        404: {
            "description": "Объявление не найдено",
        },
        500: {
            "description": "Внутренняя ошибка сервиса",
        },
    },
)

async def simple_predict(
    item_id: int = Query(ge=0),
    service: PredictionService = Depends(get_prediction_service),
    conn: asyncpg.Connection = Depends(get_db_connection),
) -> bool:
    """Проверить объявление по его идентификатору."""

    try:
        repository = ItemRepository(conn)

        # Получаем данные объявления и продавца одним запросом
        row = await repository.get_prediction_data(item_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
            )

        # Формируем запрос для существующей модели
        request = PredictionRequest(
            seller_id=row["seller_id"],
            is_verified_seller=row["is_verified_seller"],
            item_id=row["item_id"],
            name=row["name"],
            description=row["description"],
            category=row["category"],
            images_qty=row["images_qty"],
        )

        # Используем бизнес-логику первого ДЗ
        return service.predict(request)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed",
        ) from exc