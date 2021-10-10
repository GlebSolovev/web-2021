from typing import Dict

from bank_service.bank_pb2 import (
    OperationStatus,
    TransactionResponse,
    BalanceResponse,
    AddUserResponse,
)
import bank_service.bank_pb2_grpc as bank_pb2_grpc

database: Dict[int, int] = {}
MAX_STORAGE_SIZE = 10 ** 5


class BankService(bank_pb2_grpc.BankServicer):

    def ApplyTransaction(self, request, context):
        if request.from_user_id not in database or request.to_user_id not in database:
            return TransactionResponse(status=OperationStatus.USER_NOT_FOUND)
        if request.from_user_id == request.to_user_id:
            return TransactionResponse(status=OperationStatus.SELF_TRANSACTION)
        if database[request.from_user_id] < request.coins:
            return TransactionResponse(status=OperationStatus.NOT_ENOUGH_COINS)
        database[request.from_user_id] -= request.coins
        database[request.to_user_id] += request.coins
        return TransactionResponse(status=OperationStatus.SUCCESS)

    def GetBalance(self, request, context):
        if request.user_id not in database:
            return BalanceResponse(status=OperationStatus.USER_NOT_FOUND)
        return BalanceResponse(balance=database[request.user_id], status=OperationStatus.SUCCESS)

    def AddUser(self, request, context):
        new_user_id = len(database)
        if len(database) == MAX_STORAGE_SIZE:
            return AddUserResponse(status=OperationStatus.STORAGE_IS_FULL)
        database[new_user_id] = request.balance
        return AddUserResponse(user_id=new_user_id, status=OperationStatus.SUCCESS)
