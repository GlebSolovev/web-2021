from fastapi import Query, status, APIRouter
from fastapi.responses import JSONResponse

from app.models.pydantic_models import Item, TooLowPriceApiException

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello, you're at the root!"}


@router.get("/api/")
async def read_user_id(
        user_id: int = Query(..., alias="id")):
    item = {"user_id": user_id}
    return item


@router.get("/api/{user_id}")
async def read_user_id(user_id: int):
    item = {"user_id": user_id}
    return item


@router.post("/api/", responses={
    status.HTTP_405_METHOD_NOT_ALLOWED: {"model": TooLowPriceApiException}})
async def apply_discount(item: Item):
    item_dict = item.dict()
    item_dict["price"] *= 0.8
    item_dict["item_name"] += " (Discount applied)"
    if item_dict["price"] < 1:
        return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            content=TooLowPriceApiException().dict())
    return item_dict
