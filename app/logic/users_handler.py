from datetime import datetime, timezone

from app.logic.database import UsersDatabase
from app.logic.exceptions import BadCoinsNumberException, SelfTransactionsAreForbiddenException
from app.logic.user import User


class UsersHandler:
    KEYS_LEN = 100
    MAX_USERS_LIMIT = 100_000

    def __init__(self):
        self.database: UsersDatabase = UsersDatabase(self.MAX_USERS_LIMIT)
        self.initial_user: User = User(key=User.generate_new_key(self.KEYS_LEN), user_id=0, name="admin",
                                       wish="My dream is to develop this app!", karma=1)
        self.database.add_new_user(self.initial_user)

        self.last_happy_user_update_date: str = ""
        self.happy_user_id: int = -1

    def get_happy_user(self) -> User:
        current_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        if current_date != self.last_happy_user_update_date:
            self.happy_user_id = self.database.get_new_happy_user_id()
            self.last_happy_user_update_date = current_date
        return self.database.get_user_by_id(self.happy_user_id)

    def add_new_user(self, new_user_name: str, new_user_wish: str) -> User:
        new_user_id = self.database.get_users_number()
        new_user_key = User.generate_new_key(self.KEYS_LEN)
        while self.database.check_key_already_exists(new_user_key):
            new_user_key = User.generate_new_key(self.KEYS_LEN)
        new_user = User(key=new_user_key, user_id=new_user_id, name=new_user_name, wish=new_user_wish)

        self.database.add_new_user(new_user)
        return new_user

    def get_user(self, secret_key: str) -> User:
        return self.database.get_user_by_key(secret_key)

    def apply_transaction(self, from_user: User, to_user: User, coins: int) -> None:
        if from_user.id == to_user.id:
            raise SelfTransactionsAreForbiddenException
        if from_user.get_balance() < coins or coins <= 0:
            raise BadCoinsNumberException
        from_user.change_balance(-coins)
        to_user.change_balance(coins)

        from_user.increase_karma(coins)
        self.database.update_user_in_karma_list(from_user.id, coins)
