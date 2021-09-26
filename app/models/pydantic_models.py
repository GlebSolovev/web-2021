from pydantic import BaseModel


class User(BaseModel):
    name: str
    wish: str


class UsersLimitHasReachedErrorResponse(BaseModel):
    message: str = "Database is full, no more new users are allowed"


class NoSuchUserErrorResponse(BaseModel):
    message: str = "Incorrect secret key, no such user in database"


class NotEnoughCoinsErrorResponse(BaseModel):
    message: str = "Not enough coins on the balance"
