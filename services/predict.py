from repositories.prediction import PredictionRepository
from schemas.predict import PredictionRequest


class PredictionService:
    def __init__(self, repository: PredictionRepository | None = None) -> None:
        self.repository = repository or PredictionRepository()

    def predict(self, request: PredictionRequest) -> bool:
        """Coordinate prediction and return whether a violation is present."""
        return self.repository.predict_violation(request)
