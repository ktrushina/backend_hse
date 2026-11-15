import pytest

from repositories.prediction import PredictionRepository
from schemas.predict import PredictionRequest
from services.predict import PredictionService


class StubPredictionRepository(PredictionRepository):
    def get_min_images_for_unverified_seller(self) -> int:
        return 2


@pytest.mark.parametrize(
    ("is_verified_seller", "images_qty", "expected"),
    [
        (True, 0, False),
        (False, 0, True),
        (False, 1, True),
        (False, 2, False),
    ],
)
def test_service_predict(is_verified_seller, images_qty, expected):
    service = PredictionService(repository=StubPredictionRepository())
    request = PredictionRequest(
        seller_id=10,
        is_verified_seller=is_verified_seller,
        item_id=20,
        name="Chair",
        description="A comfortable chair",
        category=3,
        images_qty=images_qty,
    )

    assert service.predict(request) is expected
