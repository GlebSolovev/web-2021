from fastapi import status, APIRouter
from fastapi.responses import JSONResponse

from app.logic.exceptions import NoSuchUserException, NotEnoughCoinsException, UsersLimitHasReachedException
from app.logic.process_users import get_user, add_new_user, get_happy_user, apply_transaction
from app.models.pydantic_models import User, UsersLimitHasReachedErrorResponse, NoSuchUserErrorResponse, \
    NotEnoughCoinsErrorResponse

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Hello, you're at the root of \"One day - one happy person\" app!\n\n"
                   "Check the end-points documentation at /docs"}


@router.get("/happy-person")
async def read_happy_user():
    happy_user = get_happy_user()
    return happy_user.get_public_info()


@router.post("/new-user", responses={
    status.HTTP_507_INSUFFICIENT_STORAGE: {"model": UsersLimitHasReachedErrorResponse}})
async def register_new_user(new_user: User):
    new_user_dict = new_user.dict()
    try:
        user = add_new_user(new_user_dict["name"], new_user_dict["wish"])
        return user.get_secret_key_info()
    except UsersLimitHasReachedException:
        return JSONResponse(status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                            content=UsersLimitHasReachedErrorResponse().dict())


@router.get("/user/{secret_key}", responses={
    status.HTTP_403_FORBIDDEN: {"model": NoSuchUserErrorResponse}})
async def read_user(secret_key: str):
    try:
        user = get_user(secret_key)
        return user.get_full_info()
    except NoSuchUserException:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content=NoSuchUserErrorResponse().dict())


@router.post("/user/{secret_key}/support/{coins}", responses={
    status.HTTP_403_FORBIDDEN: {"model": NoSuchUserErrorResponse},
    status.HTTP_400_BAD_REQUEST: {"model": NotEnoughCoinsErrorResponse}})
async def support_happy_person(secret_key: str, coins: int):
    try:
        user = get_user(secret_key)
        apply_transaction(user, get_happy_user(), coins)
        success_message = {"message": "Operation succeed!"}
        return success_message
    except NoSuchUserException:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content=NoSuchUserErrorResponse().dict())
    except NotEnoughCoinsException:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=NotEnoughCoinsErrorResponse().dict())
