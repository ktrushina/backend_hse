from fastapi import APIRouter, Depends, HTTPException

from schemas.predict import PredictionRequest
from services.predict import PredictionService

router = APIRouter()


def get_prediction_service() -> PredictionService:
    return PredictionService()


@router.post(
    "/predict",
    response_model=bool,
    responses={
        400: {
            "description": "Некорректные входные данные",
        },
        500: {
            "description": "Внутренняя ошибка предсказания",
        },
    },
)
async def predict(
    request: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> bool:
    """Return true when the ad is predicted to contain a violation."""
    try:
        return service.predict(request)
    except Exception as exc:
        # do not expose internal exception details to API clients
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
