from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from graphene import Schema
from starlette.graphql import GraphQLApp

from app.logic.exceptions import NoSuchUserException, BadCoinsNumberException, UsersLimitHasReachedException, \
    SelfTransactionsAreForbiddenException
from app.logic.global_env import GlobalEnv
from app.models.graphene_models import Query
from app.models.pydantic_models import User, UsersLimitHasReachedErrorResponse, NoSuchUserErrorResponse, \
    BadCoinsNumberErrorResponse, SelfTransactionsAreForbiddenErrorResponse

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Hello, you're at the root of \"One day - one happy person\" app!\n"
                   "Check the end-points documentation at /docs"}


@router.get("/happy-person")
async def read_happy_user():
    happy_user = GlobalEnv.handler.get_happy_user()
    return GlobalEnv.handler.get_public_info(happy_user)


@router.post("/new-user", responses={
    status.HTTP_507_INSUFFICIENT_STORAGE: {"model": UsersLimitHasReachedErrorResponse}})
async def register_new_user(new_user: User):
    new_user_dict = new_user.dict()
    try:
        user = GlobalEnv.handler.add_new_user(new_user_dict["name"], new_user_dict["wish"])
        return user.get_secret_key_info()
    except UsersLimitHasReachedException:
        return JSONResponse(status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                            content=UsersLimitHasReachedErrorResponse().dict())


@router.get("/user/{secret_key}", responses={
    status.HTTP_404_NOT_FOUND: {"model": NoSuchUserErrorResponse}})
async def read_user(secret_key: str):
    try:
        user = GlobalEnv.handler.get_user(secret_key)
        return GlobalEnv.handler.get_full_info(user)
    except NoSuchUserException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=NoSuchUserErrorResponse().dict())


@router.post("/user/{secret_key}/support/{coins}", responses={
    status.HTTP_404_NOT_FOUND: {"model": NoSuchUserErrorResponse},
    status.HTTP_403_FORBIDDEN: {"model": SelfTransactionsAreForbiddenErrorResponse},
    status.HTTP_400_BAD_REQUEST: {"model": BadCoinsNumberErrorResponse}})
async def support_happy_person(secret_key: str, coins: int):
    try:
        user = GlobalEnv.handler.get_user(secret_key)
        GlobalEnv.handler.apply_transaction(user, GlobalEnv.handler.get_happy_user(), coins)
        success_message = {"message": "Operation succeed!"}
        return success_message
    except NoSuchUserException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=NoSuchUserErrorResponse().dict())
    except SelfTransactionsAreForbiddenException:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content=SelfTransactionsAreForbiddenErrorResponse().dict())
    except BadCoinsNumberException:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=BadCoinsNumberErrorResponse().dict())


router.add_route("/happy-persons-records", GraphQLApp(schema=Schema(query=Query, auto_camelcase=False)))
