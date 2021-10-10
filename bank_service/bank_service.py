from typing import Dict

from bank_service.bank_pb2 import (
    TransactionResponse,
    BalanceResponse,
    AddBankUserResponse,
)
from utils.utils_pb2 import OperationStatus
import bank_service.bank_pb2_grpc as bank_pb2_grpc


class BankService(bank_pb2_grpc.BankServicer):

    def __init__(self, max_limit: int = 100_000):
        self.max_limit: int = max_limit
        self.__database: Dict[int, int] = {}

    def ApplyTransaction(self, request, context):
        if request.from_user_id not in self.__database or request.to_user_id not in self.__database:
            return TransactionResponse(status=OperationStatus.USER_NOT_FOUND)
        if request.from_user_id == request.to_user_id:
            return TransactionResponse(status=OperationStatus.SELF_TRANSACTION)
        if self.__database[request.from_user_id] < request.coins:
            return TransactionResponse(status=OperationStatus.NOT_ENOUGH_COINS)
        self.__database[request.from_user_id] -= request.coins
        self.__database[request.to_user_id] += request.coins
        return TransactionResponse(status=OperationStatus.SUCCESS)

    def GetBalance(self, request, context):
        if request.user_id not in self.__database:
            return BalanceResponse(status=OperationStatus.USER_NOT_FOUND)
        return BalanceResponse(balance=self.__database[request.user_id], status=OperationStatus.SUCCESS)

    def AddBankUser(self, request, context):
        new_user_id = len(self.__database)
        if len(self.__database) == self.max_limit:
            return AddBankUserResponse(status=OperationStatus.STORAGE_IS_FULL)
        self.__database[new_user_id] = request.balance
        return AddBankUserResponse(user_id=new_user_id, status=OperationStatus.SUCCESS)
