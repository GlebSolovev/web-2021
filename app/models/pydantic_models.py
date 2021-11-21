from pydantic import BaseModel


class User(BaseModel):
    name: str
    wish: str


class UsersLimitHasReachedErrorResponse(BaseModel):
    message: str = "Database is full, no more new users are allowed"


class NoSuchUserErrorResponse(BaseModel):
    message: str = "Incorrect secret key, no such user in storage"


class SelfTransactionsAreForbiddenErrorResponse(BaseModel):
    message: str = "Self transactions are forbidden"


class BadCoinsNumberErrorResponse(BaseModel):
    message: str = "Number of coins must be > 0 and <= balance"
