from schemas.predict import PredictionRequest


class PredictionRepository:
    """Naive prediction backend; replace this with a model or data store later."""

    def predict_violation(self, request: PredictionRequest) -> bool:
        # Verified sellers are assumed safe. Other sellers need at least one image.
        return not request.is_verified_seller and request.images_qty == 0
