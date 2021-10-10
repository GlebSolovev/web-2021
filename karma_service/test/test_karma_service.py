from typing import List, Tuple

from karma_service.karma_pb2 import KarmaRequest, AddKarmaUserRequest, ChooseUsersRequest, ModifyKarmaRequest
from karma_service.karma_service import KarmaService
from utils.utils_pb2 import OperationStatus


def generate_karma(n: int, start: int = 0) -> List[int]:
    return [karma for karma in range(start, start + n)]


def test_empty_get():
    service = KarmaService()
    request = KarmaRequest(user_id=5)
    response = service.GetKarma(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND


def test_simple_add_new_user():
    service = KarmaService()
    karma = generate_karma(1)[0]
    request = AddKarmaUserRequest(karma=karma)
    response = service.AddKarmaUser(request, None)
    assert response.status == OperationStatus.SUCCESS


def test_simple_add_and_get():
    service = KarmaService()
    karma = generate_karma(1)[0]
    request = AddKarmaUserRequest(karma=karma)
    user_id = service.AddKarmaUser(request, None).user_id

    request = KarmaRequest(user_id=user_id)
    response = service.GetKarma(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert response.karma == karma


def test_add_and_get_complex():
    service = KarmaService()
    n = 100
    for rep in range(5):
        karmas = generate_karma(n, rep * n)
        user_ids = []
        for karma in karmas:
            request = AddKarmaUserRequest(karma=karma)
            response = service.AddKarmaUser(request, None)
            assert response.status == OperationStatus.SUCCESS
            user_ids.append(response.user_id)

        for i in range(n):
            request = KarmaRequest(user_id=user_ids[i])
            response = service.GetKarma(request, None)
            assert response.status == OperationStatus.SUCCESS
            assert response.karma == karmas[i]

            request = KarmaRequest(user_id=n * (rep + 1))
            response = service.GetKarma(request, None)
            assert response.status == OperationStatus.USER_NOT_FOUND


def test_add_user_make_database_full():
    service = KarmaService(max_limit=1)
    karma = generate_karma(1)[0]
    request = AddKarmaUserRequest(karma=karma)
    response = service.AddKarmaUser(request, None)
    assert response.status == OperationStatus.SUCCESS

    request = AddKarmaUserRequest(karma=karma)
    response = service.AddKarmaUser(request, None)
    assert response.status == OperationStatus.STORAGE_IS_FULL


def test_choose_single_user_simple():
    service = KarmaService()

    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    service.AddKarmaUser(AddKarmaUserRequest(karma=0), None)
    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    user_id = service.AddKarmaUser(AddKarmaUserRequest(karma=1), None).user_id
    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert len(response.user_ids) == 1
    assert response.user_ids[0] == user_id

    request = ChooseUsersRequest(forbidden_user_ids=[user_id], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND


def test_choose_multiple_users():
    service = KarmaService()

    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=2)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    service.AddKarmaUser(AddKarmaUserRequest(karma=0), None)
    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=2)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    user_a_id = service.AddKarmaUser(AddKarmaUserRequest(karma=1), None).user_id
    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=2)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    user_b_id = service.AddKarmaUser(AddKarmaUserRequest(karma=1), None).user_id
    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=2)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert len(response.user_ids) == 2
    assert set(response.user_ids) == {user_a_id, user_b_id}

    request = ChooseUsersRequest(forbidden_user_ids=[user_b_id], users_to_choose=2)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND


def test_choose_users_stress():
    service = KarmaService()
    n = 100
    k = 10
    karmas = generate_karma(n, 5)
    users = {}
    forbidden_user_ids = []

    for karma in range(1, 10):
        forbidden_user_ids.append(service.AddKarmaUser(AddKarmaUserRequest(karma=karma), None).user_id)

    for i in range(len(karmas)):
        user_id = service.AddKarmaUser(AddKarmaUserRequest(karma=karmas[i]), None).user_id
        users.update({user_id: karmas[i]})
        request = ChooseUsersRequest(forbidden_user_ids=forbidden_user_ids, users_to_choose=k)
        response = service.ChooseKarmaWeightedRandomUsers(request, None)
        if i + 1 >= k:
            assert response.status == OperationStatus.SUCCESS
            assert len(response.user_ids) == k
            for chosen_user_id in response.user_ids:
                assert users[chosen_user_id] > 0
        else:
            assert response.status == OperationStatus.USER_NOT_FOUND

    for _ in range(n):
        user_id = service.AddKarmaUser(AddKarmaUserRequest(karma=0), None).user_id
        users.update({user_id: 0})

        request = ChooseUsersRequest(forbidden_user_ids=forbidden_user_ids, users_to_choose=k)
        response = service.ChooseKarmaWeightedRandomUsers(request, None)
        assert response.status == OperationStatus.SUCCESS
        assert len(response.user_ids) == k
        for chosen_user_id in response.user_ids:
            assert users[chosen_user_id] > 0

    for i in range(0, 100_000):
        request = ChooseUsersRequest(forbidden_user_ids=forbidden_user_ids, users_to_choose=k)
        response = service.ChooseKarmaWeightedRandomUsers(request, None)
        assert response.status == OperationStatus.SUCCESS
        assert len(response.user_ids) == k
        for chosen_user_id in response.user_ids:
            assert service.GetKarma(KarmaRequest(user_id=chosen_user_id), None).karma == users[chosen_user_id]
            assert users[chosen_user_id] > 0


def test_modify_karma_simple():
    service = KarmaService()
    request = ModifyKarmaRequest(user_id=5, delta=5)
    response = service.ModifyKarma(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    karma = 10
    request = AddKarmaUserRequest(karma=karma)
    user_id = service.AddKarmaUser(request, None).user_id

    delta = 5
    karma += delta
    request = ModifyKarmaRequest(user_id=user_id, delta=delta)
    response = service.ModifyKarma(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetKarma(KarmaRequest(user_id=user_id), None).karma == karma

    delta = -10
    karma += delta
    request = ModifyKarmaRequest(user_id=user_id, delta=delta)
    response = service.ModifyKarma(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetKarma(KarmaRequest(user_id=user_id), None).karma == karma

    delta = -100
    karma += delta
    request = ModifyKarmaRequest(user_id=user_id, delta=delta)
    response = service.ModifyKarma(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert service.GetKarma(KarmaRequest(user_id=user_id), None).karma == karma


def test_modify_karma_simple_via_choice():
    service = KarmaService()
    karma = 0
    request = AddKarmaUserRequest(karma=karma)
    user_id = service.AddKarmaUser(request, None).user_id

    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.USER_NOT_FOUND

    delta = 5
    request = ModifyKarmaRequest(user_id=user_id, delta=delta)
    response = service.ModifyKarma(request, None)
    assert response.status == OperationStatus.SUCCESS

    request = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
    response = service.ChooseKarmaWeightedRandomUsers(request, None)
    assert response.status == OperationStatus.SUCCESS
    assert response.user_ids[0] == user_id


def test_random_choice_is_karma_weighted():
    service = KarmaService()
    negative_karma = -5
    zero_karma = 0
    small_karma = 1
    big_karma = 10_000

    request = AddKarmaUserRequest(karma=negative_karma)
    service.AddKarmaUser(request, None)
    request = AddKarmaUserRequest(karma=zero_karma)
    service.AddKarmaUser(request, None)

    request = AddKarmaUserRequest(karma=small_karma)
    small_user_id = service.AddKarmaUser(request, None).user_id
    request = AddKarmaUserRequest(karma=big_karma)
    big_user_id = service.AddKarmaUser(request, None).user_id

    def count_small_and_big_users_wins() -> Tuple[int, int]:
        n = 10_000
        big_cnt = 0
        small_cnt = 0
        for i in range(n):
            request_ = ChooseUsersRequest(forbidden_user_ids=[], users_to_choose=1)
            response_ = service.ChooseKarmaWeightedRandomUsers(request_, None)
            assert response_.status == OperationStatus.SUCCESS
            assert response_.user_ids[0] == small_user_id or response_.user_ids[0] == big_user_id
            if response_.user_ids[0] == big_user_id:
                big_cnt += 1
            else:
                small_cnt += 1
        return small_cnt, big_cnt

    small_res, big_res = count_small_and_big_users_wins()
    assert big_res > small_res

    delta = big_karma - 1
    request = ModifyKarmaRequest(user_id=small_user_id, delta=delta)
    service.ModifyKarma(request, None)
    request = ModifyKarmaRequest(user_id=big_user_id, delta=-delta)
    service.ModifyKarma(request, None)

    small_res, big_res = count_small_and_big_users_wins()
    assert big_res < small_res
