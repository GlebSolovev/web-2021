from datetime import datetime, timezone
from typing import Tuple

from app.logic.database import UsersDatabase
from app.logic.exceptions import NotEnoughCoinsException
from app.logic.user import User

KEYS_LEN = 100


def start_app() -> Tuple[UsersDatabase, User]:
    new_database = UsersDatabase()
    zero_user = User(key=User.generate_new_key(KEYS_LEN), user_id=0, name="admin",
                     wish="My dream is to develop this app!", karma=1)
    new_database.add_new_user(zero_user)
    return new_database, zero_user


database, initial_user = start_app()
last_happy_user_update_date: str = ""
happy_user_id: int = -1


def get_happy_user() -> User:
    global last_happy_user_update_date, happy_user_id
    current_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    if current_date != last_happy_user_update_date:
        happy_user_id = database.get_new_happy_user_id()
        last_happy_user_update_date = current_date
    return database.get_user_by_id(happy_user_id)


def add_new_user(new_user_name: str, new_user_wish: str) -> User:
    new_user_id = database.get_users_number()
    new_user_key = User.generate_new_key(KEYS_LEN)
    while not database.check_key_is_unique(new_user_key):
        new_user_key = User.generate_new_key(KEYS_LEN)
    new_user = User(key=new_user_key, user_id=new_user_id, name=new_user_name, wish=new_user_wish)

    database.add_new_user(new_user)
    return new_user


def get_user(secret_key: str) -> User:
    return database.get_user_by_key(secret_key)


def apply_transaction(from_user: User, to_user: User, coins: int):
    if from_user.get_balance() < coins:
        raise NotEnoughCoinsException
    from_user.change_balance(-coins)
    to_user.change_balance(coins)

    from_user.change_karma(coins)
    database.update_user_in_karma_list(from_user.id, coins)

    return
