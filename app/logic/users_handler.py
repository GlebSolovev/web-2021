import os
from datetime import datetime, timezone

from typing import NoReturn, Dict, Union

from users_service.users_pb2 import AddNewUserRequest, NewUser, GetUserByKeyRequest, GetUserByIdRequest
from users_service.users_pb2_grpc import UsersStub
from utils.constants import Constants
from app.logic.exceptions import BadCoinsNumberException, SelfTransactionsAreForbiddenException, \
    UsersLimitHasReachedException, NoSuchUserException
from app.logic.storage_service import StorageService
from app.logic.user import User

import grpc

from bank_service.bank_pb2 import AddBankUserRequest, BalanceRequest, TransactionRequest
from bank_service.bank_pb2_grpc import BankStub
from karma_service.karma_pb2 import AddKarmaUserRequest, ChooseUsersRequest, KarmaRequest, ModifyKarmaRequest
from karma_service.karma_pb2_grpc import KarmaStub
from utils.utils_pb2 import OperationStatus


class UsersHandler:

    @staticmethod
    def __init_bank_service_connection() -> BankStub:
        bank_service_host = os.getenv("BANK_SERVICE_HOST", "localhost")
        bank_service_channel = grpc.insecure_channel(
            f"{bank_service_host}:50051"
        )
        return BankStub(bank_service_channel)

    @staticmethod
    def __init_karma_service_connection() -> KarmaStub:
        karma_service_host = os.getenv("KARMA_SERVICE_HOST", "localhost")
        karma_service_channel = grpc.insecure_channel(
            f"{karma_service_host}:50052"
        )
        return KarmaStub(karma_service_channel)

    @staticmethod
    def __init_users_service_connection() -> UsersStub:
        users_service_host = os.getenv("USERS_SERVICE_HOST", "localhost")
        users_service_channel = grpc.insecure_channel(
            f"{users_service_host}:50053"
        )
        return UsersStub(users_service_channel)

    def create_user(self, name: str, wish: str, karma: int = Constants.INITIAL_KARMA,
                    balance: int = Constants.INITIAL_BALANCE) -> User:
        add_bank_user_request = AddBankUserRequest(balance=balance)
        add_bank_user_response = self.bank_service_client.AddBankUser(add_bank_user_request)
        status = add_bank_user_response.status
        if status == OperationStatus.STORAGE_IS_FULL:
            raise UsersLimitHasReachedException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid bank AddBankUser OperationStatus " + str(status))
        bank_id = add_bank_user_response.user_id

        add_karma_user_request = AddKarmaUserRequest(karma=karma)
        add_karma_user_response = self.karma_service_client.AddKarmaUser(add_karma_user_request)
        status = add_karma_user_response.status
        if status == OperationStatus.STORAGE_IS_FULL:
            raise UsersLimitHasReachedException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid karma AddKarmaUser OperationStatus " + str(status))
        user_id = add_karma_user_response.user_id

        add_new_user_request = AddNewUserRequest(
            new_user=NewUser(bank_id=bank_id, user_id=user_id, name=name, wish=wish))
        add_new_user_response = self.users_service_client.AddNewUser(add_new_user_request)
        status = add_new_user_response.status
        if status == OperationStatus.STORAGE_IS_FULL:
            raise UsersLimitHasReachedException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid users AddNewUser OperationStatus " + str(status))
        key = add_new_user_response.key

        return User(key=key, bank_id=bank_id, user_id=user_id, name=name, wish=wish)

    def __init__(self):
        self.bank_service_client: BankStub = self.__init_bank_service_connection()
        self.karma_service_client: KarmaStub = self.__init_karma_service_connection()
        self.users_service_client: UsersStub = self.__init_users_service_connection()
        self.initial_user: User = self.create_user(name="admin", wish="My dream is to develop this app!", karma=1)

        self.last_happy_user_update_date: str = ""
        self.happy_user_id: int = -1

        self.storage_service: StorageService = StorageService()

    def get_happy_user(self) -> User:
        current_date = datetime.now(timezone.utc).strftime(Constants.DATE_FORMAT)
        if current_date == self.last_happy_user_update_date:
            return self.__get_user_by_id(self.happy_user_id)

        choose_users_request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
        choose_users_response = self.karma_service_client.ChooseKarmaWeightedRandomUsers(choose_users_request)
        status = choose_users_response.status
        if status == OperationStatus.USER_NOT_FOUND:
            raise NoSuchUserException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid karma ChooseKarmaWeightedRandomUsers OperationStatus " + str(status))

        self.happy_user_id = choose_users_response.user_ids[0]
        self.last_happy_user_update_date = current_date

        happy_user = self.__get_user_by_id(self.happy_user_id)
        self.storage_service.add_record(current_date, happy_user)
        return happy_user

    def add_new_user(self, new_user_name: str, new_user_wish: str) -> User:
        return self.create_user(name=new_user_name, wish=new_user_wish, karma=Constants.INITIAL_KARMA)

    def get_user(self, secret_key: str) -> User:
        get_user_by_key_request = GetUserByKeyRequest(key=secret_key)
        get_user_by_key_response = self.users_service_client.GetUserByKey(get_user_by_key_request)
        status = get_user_by_key_response.status
        if status == OperationStatus.USER_NOT_FOUND:
            raise NoSuchUserException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid users GetUserByKey OperationStatus " + str(status))

        user = get_user_by_key_response.user
        return User(key=user.key, bank_id=user.bank_id, user_id=user.user_id, name=user.name, wish=user.wish)

    def __get_user_by_id(self, user_id: int) -> User:
        get_user_by_id_request = GetUserByIdRequest(user_id=user_id)
        get_user_by_id_response = self.users_service_client.GetUserById(get_user_by_id_request)
        status = get_user_by_id_response.status
        if status == OperationStatus.USER_NOT_FOUND:
            raise NoSuchUserException
        elif status != OperationStatus.SUCCESS:
            raise ValueError("invalid users GetUserById OperationStatus " + str(status))

        user = get_user_by_id_response.user
        return User(key=user.key, bank_id=user.bank_id, user_id=user.user_id, name=user.name, wish=user.wish)

    def get_public_info(self, user: User) -> Dict[str, Union[str, int]]:
        public_info = user.get_public_info()

        get_karma_request = KarmaRequest(user_id=user.get_user_id())
        get_karma_response = self.karma_service_client.GetKarma(get_karma_request)
        status = get_karma_response.status
        if status != OperationStatus.SUCCESS:
            raise ValueError("invalid karma GetKarma OperationStatus " + str(status))
        karma_service_info = {"karma": get_karma_response.karma}
        public_info.update(karma_service_info)

        return public_info

    def get_full_info(self, user: User) -> Dict[str, Union[str, int]]:
        full_info = self.get_public_info(user)
        full_info.update(user.get_private_info())

        get_balance_request = BalanceRequest(user_id=user.get_bank_id())
        get_balance_response = self.bank_service_client.GetBalance(get_balance_request)
        status = get_balance_response.status
        if status != OperationStatus.SUCCESS:
            raise ValueError("invalid bank GetBalance OperationStatus " + str(status))
        bank_service_info = {"balance": get_balance_response.balance}
        full_info.update(bank_service_info)

        return full_info

    def apply_transaction(self, from_user: User, to_user: User, coins: int) -> NoReturn:
        try:
            transaction_request = TransactionRequest(
                from_user_id=from_user.get_bank_id(), to_user_id=to_user.get_bank_id(), coins=coins)
        except ValueError:
            raise BadCoinsNumberException
        transaction_response = self.bank_service_client.ApplyTransaction(transaction_request)
        status = transaction_response.status
        if status == OperationStatus.SUCCESS:
            modify_karma_request = ModifyKarmaRequest(user_id=from_user.get_user_id(), delta=coins)
            modify_karma_response = self.karma_service_client.ModifyKarma(modify_karma_request)
            status = modify_karma_response.status
            if status != OperationStatus.SUCCESS:
                raise ValueError("invalid karma ModifyKarma OperationStatus " + str(status))
            return
        elif status == OperationStatus.SELF_TRANSACTION:
            raise SelfTransactionsAreForbiddenException
        elif status == OperationStatus.NOT_ENOUGH_COINS:
            raise BadCoinsNumberException
        elif status == OperationStatus.ZERO_COINS:
            raise BadCoinsNumberException
        else:
            raise ValueError("invalid bank OperationStatus " + str(status))
