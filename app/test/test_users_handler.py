import random
from datetime import datetime, timezone, timedelta
from typing import List

import pytest

from app.logic.exceptions import NoSuchUserException, SelfTransactionsAreForbiddenException, BadCoinsNumberException
from app.logic.user import User
from app.logic.users_handler import UsersHandler
from utils.constants import Constants


def create_karma_user(handler: UsersHandler, user_karma: int) -> User:
    return handler.create_user(name="name", wish="wish", karma=user_karma)


def generate_first_users(handler: UsersHandler, n: int) -> List[User]:
    return [handler.create_user(name=str(i), wish=str(i), karma=i, balance=i) for i in range(1, 1 + n)]


def yesterday() -> str:
    return (datetime.now(timezone.utc) - timedelta(1)).strftime("%Y%m%d")


def user_was_chosen(handler: UsersHandler, user: User, ) -> bool:
    for i in range(10_000):
        handler.last_happy_user_update_date = yesterday()
        if handler.get_happy_user() == user:
            return True
    return False


def test_init():
    handler = UsersHandler()
    assert handler.get_full_info(handler.initial_user)["karma"] > 0
    assert handler.get_happy_user() == handler.initial_user


def test_get_happy_user_at_first_day():
    handler = UsersHandler()
    assert handler.get_happy_user() == handler.initial_user
    create_karma_user(handler, 10_000)
    for i in range(10_000):
        assert handler.get_happy_user() == handler.initial_user


def test_get_happy_user_at_second_day():
    handler = UsersHandler()
    assert handler.get_happy_user() == handler.initial_user

    good_user = create_karma_user(handler, 10_000)
    assert user_was_chosen(handler, good_user)


def test_add_new_user_admin_clone():
    handler = UsersHandler()
    admin = handler.initial_user
    admin_clone = handler.add_new_user(admin.name, admin.wish)
    full_info = handler.get_full_info(admin_clone)
    assert admin_clone.name == admin.name == full_info["name"]
    assert admin_clone.wish == admin.wish == full_info["wish"]
    assert admin_clone.get_key() == full_info["secret_key"] != admin.get_key()
    assert admin_clone.get_bank_id() == full_info["bank_id"] != admin.get_bank_id()
    assert admin_clone.get_user_id() == full_info["user_id"] != admin.get_user_id()
    assert full_info["karma"] == Constants.INITIAL_KARMA
    assert full_info["balance"] == Constants.INITIAL_BALANCE


def test_add_and_get_new_user_stress():
    handler = UsersHandler()
    users = generate_first_users(handler, 1000)

    for user in users:
        new_user = handler.add_new_user(user.name, user.wish)
        user._User__key = new_user.get_key()
        user._User__bank_id = new_user.get_bank_id()
        user._User__user_id = new_user.get_user_id()
        assert new_user == user

    for user in users:
        assert handler.get_user(user.get_key()) == user


def test_get_user_wrong_key():
    handler = UsersHandler()
    pytest.raises(NoSuchUserException, handler.get_user, "some key")


def test_apply_transaction_between_user_and_admin():
    handler = UsersHandler()
    admin = handler.initial_user
    admin_info = handler.get_full_info(admin)
    admin_initial_balance = admin_info["balance"]
    user = handler.add_new_user("user", "Support admin")

    handler.apply_transaction(user, admin, Constants.INITIAL_BALANCE)
    admin_info = handler.get_full_info(admin)
    user_info = handler.get_full_info(user)
    assert admin_info["balance"] == admin_initial_balance + Constants.INITIAL_BALANCE
    assert user_info["balance"] == 0
    assert user_info["karma"] == Constants.INITIAL_BALANCE

    handler.apply_transaction(admin, user, Constants.INITIAL_BALANCE - 1)
    admin_info = handler.get_full_info(admin)
    user_info = handler.get_full_info(user)
    assert admin_info["balance"] == admin_initial_balance + 1
    assert user_info["balance"] == Constants.INITIAL_BALANCE - 1
    assert user_info["karma"] == Constants.INITIAL_BALANCE


def test_apply_transaction_increases_happiness():
    handler = UsersHandler()
    rich_user = handler.create_user(name="Rich man", wish="I want to help people", karma=0, balance=10_000)

    handler.apply_transaction(rich_user, handler.initial_user, 10_000)
    assert user_was_chosen(handler, rich_user)


def test_apply_transaction_user_to_himself():
    handler = UsersHandler()
    user = handler.add_new_user("hacker", "Infinite coins")
    pytest.raises(SelfTransactionsAreForbiddenException, handler.apply_transaction, user, user,
                  Constants.INITIAL_BALANCE)


def test_apply_transaction_bad_coins_number():
    handler = UsersHandler()
    from_user = handler.add_new_user("poor guy", "Help people")
    to_user = handler.add_new_user("user", "wish")
    pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, to_user, Constants.INITIAL_BALANCE + 1)
    pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, to_user, -1)


def test_common_scenario_stress():
    handler = UsersHandler()
    users_number = 1000
    days = 100
    transactions_number = 100
    users = []
    for i in range(users_number):
        users.append(handler.add_new_user(str(i), str(i)))
    for day in range(days):
        handler.last_happy_user_update_date = yesterday()
        happy_user = handler.get_happy_user()
        for j in range(transactions_number):
            from_user = random.choice(users)
            from_user_info = handler.get_full_info(from_user)
            coins = random.randint(-1, from_user_info["balance"] + 1)

            from_user_balance = from_user_info["balance"]
            from_user_karma = from_user_info["karma"]
            happy_user_balance = handler.get_full_info(happy_user)["balance"]

            if from_user.get_user_id() == happy_user.get_user_id():
                pytest.raises(SelfTransactionsAreForbiddenException,
                              handler.apply_transaction, from_user, happy_user, coins)
            elif coins <= 0 or coins > from_user_balance:
                pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, happy_user, coins)
            else:
                handler.apply_transaction(from_user, happy_user, coins)
                assert handler.get_user(from_user.get_key()) == from_user
                assert handler.get_user(happy_user.get_key()) == happy_user
                from_user_info = handler.get_full_info(from_user)
                happy_user_info = handler.get_full_info(happy_user)
                assert from_user_info["balance"] == from_user_balance - coins
                assert from_user_info["karma"] == from_user_karma + coins
                assert happy_user_info["balance"] == happy_user_balance + coins
