import random
from datetime import datetime, timezone, timedelta
from typing import List

import pytest

from app.logic.exceptions import NoSuchUserException, SelfTransactionsAreForbiddenException, BadCoinsNumberException
from app.logic.user import User
from app.logic.users_handler import UsersHandler


def create_karma_user(user_karma: int) -> User:
    return User(key="key", user_id=100, name="name", wish="wish", karma=user_karma, balance=20)


def generate_first_users(n: int) -> List[User]:
    return [User(key=str(i), user_id=i, name=str(i), wish="wish") for i in range(1, 1 + n)]


def yesterday() -> str:
    return (datetime.now(timezone.utc) - timedelta(1)).strftime("%Y%m%d")


def user_was_chosen(user: User, handler: UsersHandler) -> bool:
    for i in range(10_000):
        handler.last_happy_user_update_date = yesterday()
        if handler.get_happy_user() == user:
            return True
    return False


def test_init():
    handler = UsersHandler()
    assert handler.initial_user.get_karma() > 0
    assert handler.database.get_users_number() == 1
    assert handler.database.get_new_happy_user_id() == handler.initial_user.id


def test_get_happy_user_at_first_day():
    handler = UsersHandler()
    assert handler.get_happy_user() == handler.initial_user
    handler.database.add_new_user(create_karma_user(10_000))
    for i in range(10_000):
        assert handler.get_happy_user() == handler.initial_user


def test_get_happy_user_at_second_day():
    handler = UsersHandler()
    assert handler.get_happy_user() == handler.initial_user

    good_user = create_karma_user(10_000)
    handler.database.add_new_user(good_user)
    assert user_was_chosen(good_user, handler)


def test_add_new_user_admin_clone():
    handler = UsersHandler()
    admin = handler.initial_user
    admin_clone = handler.add_new_user(admin.name, admin.wish)
    assert admin_clone.name == admin.name
    assert admin_clone.wish == admin.wish
    assert admin_clone.get_key() != admin.get_key()
    assert admin_clone.id != admin.id
    assert admin_clone.get_karma() == 0
    assert admin_clone.get_balance() == User.INITIAL_BALANCE


def test_add_new_user_stress():
    handler = UsersHandler()
    database = handler.database
    users = generate_first_users(1000)

    for user in users:
        new_user = handler.add_new_user(user.name, user.wish)
        user._User__key = new_user.get_key()
        assert new_user == user

    for user in users:
        assert database.get_user_by_key(user.get_key()) == user
        assert database.get_user_by_id(user.id) == user


def test_get_user_admin():
    handler = UsersHandler()
    admin = handler.initial_user
    assert handler.get_user(admin.get_key()) == admin


def test_get_user_wrong_key():
    handler = UsersHandler()
    pytest.raises(NoSuchUserException, handler.get_user, "some key")


def test_get_user_stress():
    handler = UsersHandler()
    users = generate_first_users(1000)

    for user in users:
        new_user = handler.add_new_user(user.name, user.wish)
        user._User__key = new_user.get_key()

    for user in users:
        assert handler.get_user(user.get_key()) == user


def test_apply_transaction_between_user_and_admin():
    handler = UsersHandler()
    admin = handler.initial_user
    admin_initial_balance = admin.get_balance()
    user = handler.add_new_user("user", "Support admin")

    handler.apply_transaction(user, admin, User.INITIAL_BALANCE)
    assert admin.get_balance() == admin_initial_balance + User.INITIAL_BALANCE
    assert user.get_balance() == 0
    assert user.get_karma() == User.INITIAL_BALANCE

    handler.apply_transaction(admin, user, User.INITIAL_BALANCE - 1)
    assert admin.get_balance() == admin_initial_balance + 1
    assert user.get_balance() == User.INITIAL_BALANCE - 1
    assert user.get_karma() == User.INITIAL_BALANCE


def test_apply_transaction_between_users():
    handler = UsersHandler()
    to_user = handler.add_new_user("a", "a wish")
    from_user = handler.add_new_user("b", "b wish")

    handler.apply_transaction(from_user, to_user, 1)
    assert to_user.get_balance() == User.INITIAL_BALANCE + 1
    assert from_user.get_balance() == User.INITIAL_BALANCE - 1
    assert to_user.get_karma() == 0
    assert from_user.get_karma() == 1

    handler.apply_transaction(from_user, to_user, 1)
    assert to_user.get_balance() == User.INITIAL_BALANCE + 2
    assert from_user.get_balance() == User.INITIAL_BALANCE - 2
    assert to_user.get_karma() == 0
    assert from_user.get_karma() == 2


def test_apply_transaction_increases_happiness():
    handler = UsersHandler()
    rich_user = handler.add_new_user("Rich man", "I want to help people")
    rich_user.change_balance(10_000)

    handler.apply_transaction(rich_user, handler.initial_user, 10_000)
    assert user_was_chosen(rich_user, handler)


def test_apply_transaction_user_to_himself():
    handler = UsersHandler()
    user = handler.add_new_user("hacker", "Infinite coins")
    pytest.raises(SelfTransactionsAreForbiddenException, handler.apply_transaction, user, user, User.INITIAL_BALANCE)


def test_apply_transaction_bad_coins_number():
    handler = UsersHandler()
    from_user = handler.add_new_user("poor guy", "Help people")
    to_user = handler.add_new_user("user", "wish")
    pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, to_user, User.INITIAL_BALANCE + 1)
    pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, to_user, -1)


def test_common_scenario_stress():
    handler = UsersHandler()
    users_number = 10_000
    days = 100
    transactions_number = 1000
    users = []
    for i in range(users_number):
        users.append(handler.add_new_user(str(i), str(i)))
    for day in range(days):
        handler.last_happy_user_update_date = yesterday()
        happy_user = handler.get_happy_user()
        for j in range(transactions_number):
            from_user = random.choice(users)
            coins = random.randint(-1, from_user.get_balance() + 1)
            from_user_balance = from_user.get_balance()
            from_user_karma = from_user.get_karma()
            happy_user_balance = happy_user.get_balance()
            if from_user.id == happy_user.id:
                pytest.raises(SelfTransactionsAreForbiddenException,
                              handler.apply_transaction, from_user, happy_user, coins)
            elif coins <= 0 or coins > from_user.get_balance():
                pytest.raises(BadCoinsNumberException, handler.apply_transaction, from_user, happy_user, coins)
            else:
                handler.apply_transaction(from_user, happy_user, coins)
                assert handler.get_user(from_user.get_key()) == from_user
                assert handler.get_user(happy_user.get_key()) == happy_user
                assert from_user.get_balance() == from_user_balance - coins
                assert from_user.get_karma() == from_user_karma + coins
                assert happy_user.get_balance() == happy_user_balance + coins
