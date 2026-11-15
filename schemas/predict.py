from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    """Input fields required to assess an advertisement."""

    model_config = ConfigDict(strict=True)

    seller_id: int = Field(ge=0)
    is_verified_seller: bool
    item_id: int = Field(ge=0)
    name: str
    description: str
    category: int = Field(ge=0)
    images_qty: int = Field(ge=0)
