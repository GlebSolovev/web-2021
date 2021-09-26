import pytest

from app.logic.database import UsersDatabase
from app.logic.exceptions import NoSuchUserException, UserAlreadyExistsException, UsersLimitHasReachedException
from app.logic.user import User


def generate_unique_users(n: int, start_id: int = 0, start_karma: int = 0):
    return [User(key=str(i), user_id=i, name=str(i), wish="wish", karma=start_karma, balance=i) for i in
            range(start_id, start_id + n)]


def generate_zero_karma_unique_users(n: int, start_id: int = 0):
    return [User(key=str(i), user_id=i, name=str(i), wish="wish", karma=0, balance=i) for i in
            range(start_id, start_id + n)]


def test_empty_database_getters():
    database = UsersDatabase()
    assert database.get_users_number() == 0
    pytest.raises(NoSuchUserException, database.get_user_by_key, "some key")
    pytest.raises(NoSuchUserException, database.get_user_by_id, 0)


def test_add_and_get_simple():
    user = generate_unique_users(1)[0]
    database = UsersDatabase()
    database.add_new_user(user)
    assert database.get_users_number() == 1
    assert database.get_user_by_key(user.get_key()) == user
    assert database.get_user_by_id(user.id) == user


def test_add_and_get_complex():
    database = UsersDatabase()
    n = 100
    for rep in range(5):
        assert database.get_users_number() == rep * n
        users = generate_unique_users(n, rep * n)
        for user in users:
            database.add_new_user(user)
        assert database.get_users_number() == (rep + 1) * n
        for user in users:
            assert database.get_user_by_key(user.get_key()) == user
            assert database.get_user_by_id(user.id) == user
            pytest.raises(NoSuchUserException, database.get_user_by_key, "some key")
            pytest.raises(NoSuchUserException, database.get_user_by_id, n * (rep + 1))


def test_add_user_that_already_exists():
    database = UsersDatabase()
    user = generate_unique_users(1)[0]
    database.add_new_user(user)
    assert database.get_users_number() == 1
    pytest.raises(UserAlreadyExistsException, database.add_new_user, user)


def test_add_user_make_database_full():
    database = UsersDatabase(1)
    users = generate_unique_users(2)
    database.add_new_user(users[0])
    pytest.raises(UsersLimitHasReachedException, database.add_new_user, users[1])


def test_check_key_already_exists():
    database = UsersDatabase()
    assert not database.check_key_already_exists("new key")

    users = generate_unique_users(10)
    for user in users:
        database.add_new_user(user)
    for user in users:
        assert database.check_key_already_exists(user.get_key())

    assert not database.check_key_already_exists("some key")


def test_get_new_happy_user_id_simple():
    database = UsersDatabase()
    pytest.raises(NoSuchUserException, database.get_new_happy_user_id)

    zero_karma_user = generate_zero_karma_unique_users(1)[0]
    database.add_new_user(zero_karma_user)
    pytest.raises(NoSuchUserException, database.get_new_happy_user_id)

    good_user = generate_unique_users(n=1, start_id=1, start_karma=10)[0]
    database.add_new_user(good_user)
    assert database.get_new_happy_user_id() == good_user.id


def test_get_new_happy_user_id_stress():
    database = UsersDatabase()
    users = generate_unique_users(n=1000, start_id=0, start_karma=10)
    zero_karma_users = generate_zero_karma_unique_users(n=1000, start_id=1000)
    for user in users:
        database.add_new_user(user)
        assert database.get_user_by_id(database.get_new_happy_user_id()).get_karma() > 0
    for zero_karma_user in zero_karma_users:
        database.add_new_user(zero_karma_user)
        assert database.get_user_by_id(database.get_new_happy_user_id()).get_karma() > 0
    for i in range(0, 100_000):
        assert database.get_user_by_id(database.get_new_happy_user_id()).get_karma() > 0


def test_update_user_in_karma_list():
    database = UsersDatabase()
    user = generate_zero_karma_unique_users(1)[0]
    database.add_new_user(user)
    pytest.raises(NoSuchUserException, database.get_new_happy_user_id)

    user.increase_karma(10)
    database.update_user_in_karma_list(user.id, 10)
    assert database.get_new_happy_user_id() == user.id
