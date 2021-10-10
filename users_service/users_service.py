import secrets
import string
from typing import Dict

from users_service.users_pb2 import (
    GetUserResponse, User, AddNewUserResponse
)
import users_service.users_pb2_grpc as users_pb2_grpc
from utils.constants import Constants
from utils.utils_pb2 import OperationStatus


class UsersService(users_pb2_grpc.UsersServicer):

    def __init__(self, max_limit: int = 100_000):
        self.max_limit = max_limit
        self.__keys_to_users: Dict[str, User] = {}
        self.__ids_to_users: Dict[int, User] = {}

    def GetUserById(self, request, context):
        if request.user_id not in self.__ids_to_users:
            return GetUserResponse(status=OperationStatus.USER_NOT_FOUND)
        return GetUserResponse(user=self.__ids_to_users[request.user_id], status=OperationStatus.SUCCESS)

    def GetUserByKey(self, request, context):
        if request.key not in self.__keys_to_users:
            return GetUserResponse(status=OperationStatus.USER_NOT_FOUND)
        return GetUserResponse(user=self.__keys_to_users[request.key], status=OperationStatus.SUCCESS)

    def __generate_new_unique_key(self, key_len: int) -> str:
        def generate_new_key() -> str:
            return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_len))

        key = generate_new_key()
        while key in self.__keys_to_users:
            key = generate_new_key()
        return key

    def AddNewUser(self, request, context):
        if len(self.__keys_to_users) >= self.max_limit:
            return AddNewUserResponse(status=OperationStatus.STORAGE_IS_FULL)
        new_user = request.new_user
        if new_user.user_id in self.__ids_to_users:
            return AddNewUserResponse(status=OperationStatus.USER_ALREADY_EXISTS)

        new_user_key = self.__generate_new_unique_key(Constants.KEYS_LEN)
        user = User(key=new_user_key, bank_id=new_user.bank_id, user_id=new_user.user_id,
                    name=new_user.name, wish=new_user.wish)
        self.__keys_to_users[new_user_key] = user
        self.__ids_to_users[new_user.user_id] = user
        return AddNewUserResponse(key=new_user_key, status=OperationStatus.SUCCESS)
