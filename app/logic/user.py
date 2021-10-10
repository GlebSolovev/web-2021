import secrets
import string
from typing import Dict, Union


class User:

    def __init__(self, key: str, user_id: int, bank_id: int, name: str, wish: str, karma: int = 0):
        self.__key = key
        self.id = user_id
        self.bank_id = None
        self.name = name
        self.wish = wish
        self.__karma = karma

    @staticmethod
    def generate_new_key(key_len: int) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_len))

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def get_key(self) -> str:
        return self.__key

    def get_karma(self) -> int:
        return self.__karma

    def increase_karma(self, value: int) -> None:
        self.__karma += value

    def get_public_info(self) -> Dict[str, Union[str, int]]:
        return {"id": self.id, "name": self.name, "wish": self.wish, "karma": self.__karma}

    def get_secret_key_info(self) -> Dict[str, str]:
        return {"secret_key": self.__key}
