import secrets
import string
from typing import Dict, Union


class User:

    def __init__(self, key: str, bank_id: int, karma_id: int, name: str, wish: str):
        self.__key = key
        self.bank_id = bank_id
        self.karma_id = karma_id
        self.name = name
        self.wish = wish

    @staticmethod
    def generate_new_key(key_len: int) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_len))

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def get_key(self) -> str:
        return self.__key

    def get_public_info(self) -> Dict[str, Union[str, int]]:
        return {"name": self.name, "wish": self.wish}

    def get_secret_key_info(self) -> Dict[str, str]:
        return {"secret_key": self.__key, "bank_id": self.bank_id, "karma_id": self.karma_id}
