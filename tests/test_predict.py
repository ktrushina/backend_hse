import pytest
from fastapi.testclient import TestClient

from main import app
from routers.predict import get_prediction_service

client = TestClient(app)


def payload(**overrides):
    data = {
        "seller_id": 10,
        "is_verified_seller": False,
        "item_id": 20,
        "name": "Chair",
        "description": "A comfortable chair",
        "category": 3,
        "images_qty": 1,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"is_verified_seller": True, "images_qty": 0}, False),
        ({"is_verified_seller": True, "images_qty": 4}, False),
        ({"is_verified_seller": False, "images_qty": 1}, False),
        ({"is_verified_seller": False, "images_qty": 0}, True),
        ({"is_verified_seller": False, "images_qty": 5}, False),
    ],
)
def test_predict_rule(overrides, expected):
    response = client.post("/predict", json=payload(**overrides))

    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize(
    "overrides",
    [
        {"seller_id": "10"},
        {"is_verified_seller": 1},
        {"item_id": None},
        {"name": 12},
        {"description": None},
        {"category": "3"},
        {"images_qty": -1},
        {"images_qty": 1.5},
    ],
)
def test_invalid_field_returns_400(overrides):
    response = client.post("/predict", json=payload(**overrides))

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid request data"


@pytest.mark.parametrize("missing_field", [
    "seller_id",
    "is_verified_seller",
    "item_id",
    "name",
    "description",
    "category",
    "images_qty",
])
def test_missing_required_field_returns_400(missing_field):
    data = payload()
    del data[missing_field]

    response = client.post("/predict", json=data)

    assert response.status_code == 400


def test_business_logic_error_returns_500():
    class BrokenService:
        def predict(self, request):
            raise RuntimeError("internal error")

    app.dependency_overrides[get_prediction_service] = lambda: BrokenService()
    try:
        response = client.post("/predict", json=payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {"detail": "Prediction failed"}


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
