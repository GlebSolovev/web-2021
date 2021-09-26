import secrets
from typing import Dict, List

from app.logic.exceptions import NoSuchUserException, UsersLimitHasReachedException, UserAlreadyExistsException
from app.logic.user import User


class UsersDatabase:

    def __init__(self, max_limit: int = 100_000):
        self.max_limit = max_limit
        self.__keys_to_ids: Dict[str, int] = {}
        self.__ids_to_users: Dict[int, User] = {}
        self.__karma_list: List[int] = []  # user id occurrence = user's karma

    def add_new_user(self, new_user: User) -> None:
        if len(self.__ids_to_users) >= self.max_limit:
            raise UsersLimitHasReachedException
        if new_user.get_key() in self.__keys_to_ids or new_user.id in self.__ids_to_users:
            raise UserAlreadyExistsException

        self.__keys_to_ids[new_user.get_key()] = new_user.id
        self.__ids_to_users[new_user.id] = new_user
        for i in range(new_user.get_karma()):
            self.__karma_list.append(new_user.id)

    def get_user_by_id(self, user_id: int) -> User:
        if user_id not in self.__ids_to_users:
            raise NoSuchUserException
        return self.__ids_to_users[user_id]

    def get_user_by_key(self, key: str) -> User:
        if key not in self.__keys_to_ids:
            raise NoSuchUserException
        return self.__ids_to_users[self.__keys_to_ids[key]]

    def get_users_number(self) -> int:
        return len(self.__ids_to_users)

    def check_key_already_exists(self, new_key: str) -> bool:
        return new_key in self.__keys_to_ids

    def get_new_happy_user_id(self) -> int:
        if len(self.__karma_list) == 0:
            raise NoSuchUserException
        return secrets.choice(self.__karma_list)

    def update_user_in_karma_list(self, user_id: int, coins: int) -> None:
        for i in range(coins):
            self.__karma_list.append(user_id)
