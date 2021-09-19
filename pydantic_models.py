from pydantic import BaseModel, Field


class Item(BaseModel):
    user_name: str
    price: float = Field(..., ge=1)
    item_name: str


class Message(BaseModel):
    message: str
