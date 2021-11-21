from typing import Dict, Union


class User:

    def __init__(self, key: str, bank_id: int, user_id: int, name: str, wish: str):
        self.__key = key
        self.__bank_id = bank_id
        self.__user_id = user_id
        self.name = name
        self.wish = wish

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def get_key(self) -> str:
        return self.__key

    def get_bank_id(self) -> int:
        return self.__bank_id

    def get_user_id(self) -> int:
        return self.__user_id

    def get_public_info(self) -> Dict[str, Union[str, int]]:
        return {"name": self.name, "wish": self.wish}

    def get_private_info(self) -> Dict[str, Union[str, int]]:
        return {"secret_key": self.__key, "bank_id": self.__bank_id, "user_id": self.__user_id}

    def get_secret_key_info(self) -> Dict[str, str]:
        return {"secret_key": self.__key}
