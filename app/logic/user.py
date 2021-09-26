import secrets
import string


class User:
    INIT_BALANCE: int = 100

    def __init__(self, key: str, user_id: int, name: str, wish: str, karma: int = 0, balance: int = INIT_BALANCE):
        self.__key = key
        self.id = user_id
        self.name = name
        self.wish = wish
        self.__karma = karma
        self.__balance = balance

    @staticmethod
    def generate_new_key(key_len: int):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_len))

    def get_key(self):
        return self.__key

    def get_karma(self):
        return self.__karma

    def change_karma(self, delta: int):
        self.__karma += delta

    def get_balance(self):
        return self.__balance

    def change_balance(self, delta: int):
        self.__balance += delta

    def get_public_info(self):
        return {"id": self.id, "name": self.name, "wish": self.wish, "karma": self.__karma}

    def get_full_info(self):
        info = self.get_public_info()
        info["secret_key"] = self.__key
        info["balance"] = self.__balance
        return info

    def get_secret_key_info(self):
        return {"secret_key": self.__key}
