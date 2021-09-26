from app.logic.user import User


def create_default_user() -> User:
    return User(key="key", user_id=0, name="name", wish="wish", karma=10, balance=20)


def test_user_creation_and_getters():
    user = create_default_user()
    assert user.get_key() == "key"
    assert user.get_karma() == 10
    assert user.get_balance() == 20


def test_user_increase_karma():
    user = create_default_user()
    user.increase_karma(10)
    assert user.get_karma() == 20


def test_user_change_balance():
    user = create_default_user()
    user.change_balance(10)
    assert user.get_balance() == 30
    user.change_balance(-50)
    assert user.get_balance() == -20


def test_generate_new_key():
    key = User.generate_new_key(10)
    assert len(key) == 10
    assert key.isalnum()
