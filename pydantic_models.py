from pydantic import BaseModel, Field


class Item(BaseModel):
    user_name: str
    price: float = Field(..., ge=1)
    item_name: str


class TooLowPriceApiException(BaseModel):
    message: str = "Price became too low, min=1."
