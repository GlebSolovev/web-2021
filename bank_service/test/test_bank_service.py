from typing import List

from bank_service.bank_pb2 import BalanceRequest, AddBankUserRequest, TransactionRequest
from bank_service.bank_service import BankService
from utils.utils_pb2 import OperationStatus


def generate_balances(n: int, start: int = 0) -> List[int]:
    return [balance for balance in range(start, start + n)]


def test_empty_get():
    service = BankService()
    request = BalanceRequest(user_id=5)
    response = service.GetBalance(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND


def test_simple_add_new_user():
    service = BankService()
    balance = generate_balances(1)[0]
    request = AddBankUserRequest(balance=balance)
    response = service.AddBankUser(request, None)
    assert response.status == OperationStatus.SUCCESS


def test_simple_add_and_get():
    service = BankService()
    balance = generate_balances(1)[0]
    request = AddBankUserRequest(balance=balance)
    user_id = service.AddBankUser(request, None).user_id

    request = BalanceRequest(user_id=user_id)
    response = service.GetBalance(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert response.balance == balance


def test_add_and_get_complex():
    service = BankService()
    n = 100
    for rep in range(5):
        balances = generate_balances(n, rep * n)
        user_ids = []
        for balance in balances:
            request = AddBankUserRequest(balance=balance)
            response = service.AddBankUser(request, None)
            assert response.status == OperationStatus.SUCCESS
            user_ids.append(response.user_id)

        for i in range(n):
            request = BalanceRequest(user_id=user_ids[i])
            response = service.GetBalance(request, None)
            assert response.status == OperationStatus.SUCCESS
            assert response.balance == balances[i]

            request = BalanceRequest(user_id=n * (rep + 1))
            response = service.GetBalance(request, None)
            assert response.status == OperationStatus.USER_NOT_FOUND


def test_add_user_make_database_full():
    service = BankService(max_limit=1)
    balance = generate_balances(1)[0]
    request = AddBankUserRequest(balance=balance)
    response = service.AddBankUser(request, None)
    assert response.status == OperationStatus.SUCCESS

    request = AddBankUserRequest(balance=balance)
    response = service.AddBankUser(request, None)
    assert response.status == OperationStatus.STORAGE_IS_FULL


def test_apply_transaction_fails():
    service = BankService()
    request = TransactionRequest(from_user_id=0, to_user_id=1, coins=10)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    from_user_balance = 5
    from_user_id = service.AddBankUser(AddBankUserRequest(balance=from_user_balance), None).user_id
    request = TransactionRequest(from_user_id=from_user_id, to_user_id=1, coins=10)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    to_user_balance = 0
    to_user_id = service.AddBankUser(AddBankUserRequest(balance=to_user_balance), None).user_id
    request = TransactionRequest(from_user_id=100, to_user_id=to_user_id, coins=10)  # suppose there is no user_id = 100
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    request = TransactionRequest(from_user_id=from_user_id, to_user_id=to_user_id, coins=2 * from_user_balance)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.NOT_ENOUGH_COINS

    request = TransactionRequest(from_user_id=from_user_id, to_user_id=from_user_id, coins=from_user_balance)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.SELF_TRANSACTION


# noinspection DuplicatedCode
def test_apply_transaction_simple():
    service = BankService()
    from_user_balance = 5
    to_user_balance = 0
    delta = from_user_balance - 1

    from_user_id = service.AddBankUser(AddBankUserRequest(balance=from_user_balance), None).user_id
    to_user_id = service.AddBankUser(AddBankUserRequest(balance=to_user_balance), None).user_id

    from_user_balance -= delta
    to_user_balance += delta

    request = TransactionRequest(from_user_id=from_user_id, to_user_id=to_user_id, coins=delta)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetBalance(BalanceRequest(user_id=from_user_id), None).balance == from_user_balance
    assert service.GetBalance(BalanceRequest(user_id=to_user_id), None).balance == to_user_balance

    request = TransactionRequest(from_user_id=from_user_id, to_user_id=to_user_id, coins=0)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetBalance(BalanceRequest(user_id=from_user_id), None).balance == from_user_balance
    assert service.GetBalance(BalanceRequest(user_id=to_user_id), None).balance == to_user_balance

    from_user_balance += delta
    to_user_balance -= delta

    request = TransactionRequest(from_user_id=to_user_id, to_user_id=from_user_id, coins=delta)
    response = service.ApplyTransaction(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetBalance(BalanceRequest(user_id=from_user_id), None).balance == from_user_balance
    assert service.GetBalance(BalanceRequest(user_id=to_user_id), None).balance == to_user_balance
