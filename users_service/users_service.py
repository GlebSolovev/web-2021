import secrets
import string

from users_service.users_pb2 import (
    GetUserResponse, User, AddNewUserResponse
)
import users_service.users_pb2_grpc as users_pb2_grpc
from utils.constants import Constants
from utils.sqlite import execute_query, create_connection, execute_read_query
from utils.utils_pb2 import OperationStatus


# noinspection SqlNoDataSourceInspection,SqlResolve
class UsersService(users_pb2_grpc.UsersServicer):

    def __create_tables(self):
        drop_users_table = "DROP TABLE IF EXISTS users;"
        create_users_table = """
            CREATE TABLE users (          
                id INTEGER PRIMARY KEY,
                bank_id INTEGER,
                name TEXT NOT NULL,
                wish TEXT NOT NULL
            );
        """
        drop_keys_table = "DROP TABLE IF EXISTS keys;"
        create_keys_table = """
            CREATE TABLE keys (          
                key TEXT NOT NULL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """
        drop_bank_ids_table = "DROP TABLE IF EXISTS bank_ids;"
        create_bank_ids_table = """
            CREATE TABLE bank_ids (          
                bank_id INTEGER NOT NULL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """
        execute_query(self.connection, drop_users_table)
        execute_query(self.connection, create_users_table)
        execute_query(self.connection, drop_keys_table)
        execute_query(self.connection, create_keys_table)
        execute_query(self.connection, drop_bank_ids_table)
        execute_query(self.connection, create_bank_ids_table)
        print("ok")

    def __init__(self, max_limit: int = Constants.MAX_USERS_LIMIT):
        self.max_limit = max_limit
        self.connection = create_connection(Constants.USERS_SQL_LITE_DB_PATH)
        self.__create_tables()
        self.users_number = 0  # TODO: get size from users table

    def __get_user(self, where_condition: str) -> User:
        select_user = f"""
            SELECT
                keys.key,
                bank_ids.bank_id,
                users.id,
                users.name,
                users.wish
            FROM
                users
                INNER JOIN keys ON users.id = keys.user_id
                INNER JOIN bank_ids ON users.id = bank_ids.user_id
            WHERE {where_condition}
        """
        user = execute_read_query(self.connection, select_user)
        if len(user) == 0:
            return None
        key, bank_id, user_id, name, wish = user[0]
        return User(key=key, bank_id=bank_id, user_id=user_id, name=name, wish=wish)

    def GetUserById(self, request, context):
        user = self.__get_user(f"users.id == {request.user_id}")
        if user is None:
            return GetUserResponse(status=OperationStatus.USER_NOT_FOUND)
        return GetUserResponse(user=user, status=OperationStatus.SUCCESS)

    def GetUserByKey(self, request, context):
        user = self.__get_user(f"""keys.key == '{request.key}'""")
        if user is None:
            return GetUserResponse(status=OperationStatus.USER_NOT_FOUND)
        return GetUserResponse(user=user, status=OperationStatus.SUCCESS)

    def __check_key_in_keys(self, key: str) -> bool:
        select_key = f"""
            SELECT keys.key
            FROM keys
            WHERE keys.key = '{key}'
        """
        selected_key = execute_read_query(self.connection, select_key)
        return len(selected_key) != 0

    def __generate_new_unique_key(self, key_len: int) -> str:
        def generate_new_key() -> str:
            return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(key_len))

        key = generate_new_key()
        while self.__check_key_in_keys(key):
            key = generate_new_key()
        return key

    def __check_id_in_users(self, user_id: int) -> bool:
        select_id = f"""
            SELECT users.id
            FROM users
            WHERE users.id = {user_id}
        """
        selected_id = execute_read_query(self.connection, select_id)
        return len(selected_id) != 0

    def AddNewUser(self, request, context):
        if self.users_number == self.max_limit:
            return AddNewUserResponse(status=OperationStatus.STORAGE_IS_FULL)
        new_user = request.new_user
        if self.__check_id_in_users(new_user.user_id):
            return AddNewUserResponse(status=OperationStatus.USER_ALREADY_EXISTS)

        new_user_key = self.__generate_new_unique_key(Constants.KEYS_LEN)
        user = User(key=new_user_key, bank_id=new_user.bank_id, user_id=new_user.user_id,
                    name=new_user.name, wish=new_user.wish)

        create_user = f"""
            INSERT INTO users (id, bank_id, name, wish)
            VALUES ({user.user_id}, {user.bank_id}, '{user.name}', '{user.wish}');
        """
        create_key = f"""
            INSERT INTO keys (key, user_id)
            VALUES ('{user.key}',{user.user_id});
        """
        create_bank_id = f"""
            INSERT INTO bank_ids (bank_id, user_id)
            VALUES ({user.bank_id}, {user.user_id});
        """
        execute_query(self.connection, create_user)
        execute_query(self.connection, create_key)
        execute_query(self.connection, create_bank_id)

        self.users_number += 1
        return AddNewUserResponse(key=new_user_key, status=OperationStatus.SUCCESS)
