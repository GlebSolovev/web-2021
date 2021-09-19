from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class Item(BaseModel):
    user_name: str
    price: float = Field(..., ge=1)
    item_name: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, you're at the root!"}


@app.get("/api/")
async def read_user_id(
        user_id: int = Query(..., alias="id")):
    item = {"user_id": user_id}
    return item


@app.get("/api/{user_id}")
async def read_user_id(user_id: int):
    item = {"user_id": user_id}
    return item


@app.post("/api/", responses={
    status.HTTP_405_METHOD_NOT_ALLOWED: {"model": Message, "description": "Price became too low, min=1."}})
async def apply_discount(item: Item):
    item_dict = item.dict()
    item_dict["price"] *= 0.8
    item_dict["item_name"] += " (Discount applied)"
    if item_dict["price"] < 1:
        return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            content={"message": "Price became too low, min=1."})
    return item_dict
