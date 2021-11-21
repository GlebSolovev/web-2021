from app.logic.user import User


def test_user_creation_and_getters():
    user = User(key="key", bank_id=10, user_id=20, name="name", wish="wish")
    assert user.get_key() == "key"
    assert user.get_bank_id() == 10
    assert user.get_user_id() == 20
    assert user.name == "name"
    assert user.wish == "wish"
