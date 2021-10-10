import secrets
from typing import Dict, List

from app.logic.exceptions import NoSuchUserException, UsersLimitHasReachedException, UserAlreadyExistsException
from app.logic.user import User


class UsersDatabase:

    def __init__(self, max_limit: int = 100_000):
        self.max_limit = max_limit
        self.__keys_to_users: Dict[str, User] = {}
        self.__karma_ids_to_users: Dict[int, User] = {}

    def add_new_user(self, new_user: User) -> None:
        if len(self.__keys_to_users) >= self.max_limit:
            raise UsersLimitHasReachedException
        if new_user.get_key() in self.__keys_to_users or new_user.karma_id in self.__karma_ids_to_users:
            raise UserAlreadyExistsException
        self.__keys_to_users[new_user.get_key()] = new_user
        self.__karma_ids_to_users[new_user.karma_id] = new_user

    def get_user_by_key(self, key: str) -> User:
        if key not in self.__keys_to_users:
            raise NoSuchUserException
        return self.__keys_to_users[key]

    def get_user_by_karma_id(self, karma_id: int) -> User:
        if karma_id not in self.__karma_ids_to_users:
            raise NoSuchUserException
        return self.__karma_ids_to_users[karma_id]

    def get_users_number(self) -> int:
        return len(self.__keys_to_users)

    def check_key_already_exists(self, new_key: str) -> bool:
        return new_key in self.__keys_to_users
