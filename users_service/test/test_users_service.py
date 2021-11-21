from typing import List

from users_service.users_pb2 import AddNewUserRequest, User, NewUser, GetUserByKeyRequest, GetUserByIdRequest
from users_service.users_service import UsersService
from utils.utils_pb2 import OperationStatus


def generate_users(n: int, start: int = 0) -> List[NewUser]:
    return [NewUser(bank_id=i, user_id=i, name=str(i), wish="wish") for i in range(start, start + n)]


def compare_new_user_to_user(new_user: NewUser, user: User) -> bool:
    return new_user.bank_id == user.bank_id and new_user.user_id == user.user_id \
           and new_user.name == user.name and new_user.wish == user.wish


def test_empty_getters():
    service = UsersService()
    request = GetUserByKeyRequest(key="some key")
    response = service.GetUserByKey(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    request = GetUserByIdRequest(user_id=5)
    response = service.GetUserById(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND


def test_simple_add_new_user():
    service = UsersService()
    new_user = generate_users(1)[0]
    request = AddNewUserRequest(new_user=new_user)
    response = service.AddNewUser(request, None)
    assert response.status == OperationStatus.SUCCESS


def test_simple_add_and_get():
    service = UsersService()
    new_user = generate_users(1)[0]
    request = AddNewUserRequest(new_user=new_user)
    key = service.AddNewUser(request, None).key

    request = GetUserByKeyRequest(key=key)
    response = service.GetUserByKey(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert compare_new_user_to_user(new_user, response.user)

    request = GetUserByIdRequest(user_id=new_user.user_id)
    response = service.GetUserById(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert compare_new_user_to_user(new_user, response.user)


def test_add_and_get_complex():
    service = UsersService()
    n = 100
    for rep in range(5):
        new_users = generate_users(n, rep * n)
        keys = []
        for new_user in new_users:
            request = AddNewUserRequest(new_user=new_user)
            response = service.AddNewUser(request, None)
            assert response.status == OperationStatus.SUCCESS
            keys.append(response.key)

        for i in range(n):
            request = GetUserByKeyRequest(key=keys[i])
            response = service.GetUserByKey(request, None)
            assert response.status == OperationStatus.SUCCESS
            assert compare_new_user_to_user(new_users[i], response.user)

            request = GetUserByIdRequest(user_id=new_users[i].user_id)
            response = service.GetUserById(request, None)
            assert response.status == OperationStatus.SUCCESS
            assert compare_new_user_to_user(new_users[i], response.user)

            request = GetUserByKeyRequest(key="some key")
            response = service.GetUserByKey(request, None)
            assert response.status == OperationStatus.USER_NOT_FOUND

            request = GetUserByIdRequest(user_id=n * (rep + 1))
            response = service.GetUserById(request, None)
            assert response.status == OperationStatus.USER_NOT_FOUND


def test_add_user_that_already_exists():
    service = UsersService()
    new_user = generate_users(1)[0]
    request = AddNewUserRequest(new_user=new_user)
    response = service.AddNewUser(request, None)
    assert response.status == OperationStatus.SUCCESS

    request = AddNewUserRequest(new_user=new_user)
    response = service.AddNewUser(request, None)
    assert response.status == OperationStatus.USER_ALREADY_EXISTS


def test_add_user_make_database_full():
    service = UsersService(max_limit=1)
    new_users = generate_users(2)
    request = AddNewUserRequest(new_user=new_users[0])
    response = service.AddNewUser(request, None)
    assert response.status == OperationStatus.SUCCESS

    request = AddNewUserRequest(new_user=new_users[1])
    response = service.AddNewUser(request, None)
    assert response.status == OperationStatus.STORAGE_IS_FULL
