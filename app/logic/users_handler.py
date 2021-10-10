import os
from datetime import datetime, timezone

from typing import NoReturn, Dict, Union

from app.logic.constants import Constants
from app.logic.database import UsersDatabase
from app.logic.exceptions import BadCoinsNumberException, SelfTransactionsAreForbiddenException, \
    UsersLimitHasReachedException
from app.logic.storage_service import StorageService
from app.logic.user import User

import grpc

from bank_service.bank_pb2 import TransactionRequest, OperationStatus, AddUserRequest, BalanceRequest
from bank_service.bank_pb2_grpc import BankStub


class UsersHandler:

    @staticmethod
    def __init_bank_service_connection() -> BankStub:
        bank_service_host = os.getenv("BANK_SERVICE_HOST", "localhost")
        bank_service_channel = grpc.insecure_channel(
            f"{bank_service_host}:50051"
        )
        return BankStub(bank_service_channel)

    def __create_user(self, name: str, wish: str, karma: int) -> User:
        add_user_request = AddUserRequest(balance=Constants.INITIAL_BALANCE)
        add_user_response = self.bank_service_client.AddUser(add_user_request)
        status = add_user_response.status
        if status == OperationStatus.STORAGE_IS_FULL:
            raise UsersLimitHasReachedException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid bank AddUser OperationStatus " + str(status))

        user_id = self.database.get_users_number()
        user_key = User.generate_new_key(Constants.KEYS_LEN)
        while self.database.check_key_already_exists(user_key):
            user_key = User.generate_new_key(Constants.KEYS_LEN)

        new_user = User(key=user_key, user_id=user_id, bank_id=add_user_response.user_id,
                        name=name, wish=wish, karma=karma)
        self.database.add_new_user(new_user)
        return new_user

    def __init__(self):
        self.bank_service_client: BankStub = self.__init_bank_service_connection()
        self.database: UsersDatabase = UsersDatabase(Constants.MAX_USERS_LIMIT)
        self.initial_user: User = self.__create_user(name="admin", wish="My dream is to develop this app!", karma=1)

        self.last_happy_user_update_date: str = ""
        self.happy_user_id: int = -1

        self.storage_service: StorageService = StorageService()

    def get_happy_user(self) -> User:
        current_date = datetime.now(timezone.utc).strftime(Constants.DATE_FORMAT)
        if current_date != self.last_happy_user_update_date:
            self.happy_user_id = self.database.get_new_happy_user_id()
            self.last_happy_user_update_date = current_date
            self.storage_service.add_record(current_date,
                                            self.database.get_user_by_id(self.happy_user_id))
        return self.database.get_user_by_id(self.happy_user_id)

    def add_new_user(self, new_user_name: str, new_user_wish: str) -> User:
        return self.__create_user(name=new_user_name, wish=new_user_wish, karma=0)

    def get_user(self, secret_key: str) -> User:
        return self.database.get_user_by_key(secret_key)

    def get_full_info(self, user: User) -> Dict[str, Union[str, int]]:
        app_service_info = user.get_public_info()
        app_service_info.update(user.get_secret_key_info())

        get_balance_request = BalanceRequest(user_id=user.bank_id)
        get_balance_response = self.bank_service_client.GetBalance(get_balance_request)
        status = get_balance_response.status
        if status != OperationStatus.SUCCESS:
            raise ValueError("invalid bank GetBalance OperationStatus " + str(status))
        bank_service_info = {"balance": get_balance_response.balance}
        app_service_info.update(bank_service_info)

        return app_service_info

    def apply_transaction(self, from_user: User, to_user: User, coins: int) -> NoReturn:
        transaction_request = TransactionRequest(from_user_id=from_user.bank_id,
                                                 to_user_id=to_user.bank_id, coins=coins)
        transaction_response = self.bank_service_client.ApplyTransaction(transaction_request)
        status = transaction_response.status
        if status == OperationStatus.SUCCESS:
            from_user.increase_karma(coins)
            self.database.update_user_in_karma_list(from_user.id, coins)
            return
        elif status == OperationStatus.SELF_TRANSACTION:
            raise SelfTransactionsAreForbiddenException
        elif status == OperationStatus.NOT_ENOUGH_COINS:
            raise BadCoinsNumberException
        else:
            raise ValueError("invalid bank OperationStatus " + str(status))
