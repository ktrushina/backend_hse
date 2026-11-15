from repositories.prediction import PredictionRepository
from schemas.predict import PredictionRequest


class PredictionService:
    def __init__(self, repository: PredictionRepository | None = None) -> None:
        if repository is None:
            repository = PredictionRepository()
        self.repository = repository

    def predict(self, request: PredictionRequest) -> bool:
        if request.is_verified_seller:
            return False

        min_images = self.repository.get_min_images_for_unverified_seller()
        return request.images_qty < min_images
