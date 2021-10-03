from datetime import timedelta

import pytest
from typing import List, Tuple

from app.logic.exceptions import BadDateException
from app.logic.storage_service import StorageService, convert_to_date_str, convert_to_date_object, Record
from app.test.test_users_handler import generate_first_users


def generate_records(n: int, from_date_str: str) -> List[Record]:
    start_date = convert_to_date_object(from_date_str)
    users = generate_first_users(n)
    res = []
    for i in range(n):
        res.append((start_date + timedelta(days=i), users[i]))
    return res


def test_empty_storage():
    service = StorageService()
    date = convert_to_date_object("2021-10-03")
    pytest.raises(BadDateException, service.get_record, date)


def test_simple_add_get_record():
    service = StorageService()
    date = convert_to_date_object("2021-10-03")
    user1, user2 = generate_first_users(2)

    service.add_record(convert_to_date_str(date), user1)
    assert service.get_record(date) == (date, user1)

    service.add_record(convert_to_date_str(date), user2)
    assert service.get_record(date) == (date, user2)


# noinspection DuplicatedCode
def test_multiple_add_get_record():
    service = StorageService()
    n = 100
    start_date = convert_to_date_object("2021-10-03")
    dates = [start_date + timedelta(days=i) for i in range(n)]
    users = generate_first_users(n)

    for i in range(n):
        service.add_record(convert_to_date_str(dates[i]), users[i])
    for i in range(n):
        assert service.get_record(dates[i]) == (dates[i], users[i])


# noinspection DuplicatedCode
def test_add_get_record_over_max_limit():
    max_limit = 10
    service = StorageService(max_storage_limit=max_limit)
    n = max_limit * 10
    start_date = convert_to_date_object("2021-10-03")
    dates = [start_date + timedelta(days=i) for i in range(n)]
    users = generate_first_users(n)

    for i in range(n):
        service.add_record(convert_to_date_str(dates[i]), users[i])
    for i in range(n - max_limit):
        pytest.raises(BadDateException, service.get_record, dates[i])
    for i in range(n - max_limit, n):
        assert service.get_record(dates[i]) == (dates[i], users[i])


def query_get_records_interval(n: int, from_date_str: str, to_date_str: str, max_limit: int = 365) \
        -> Tuple[List[Record], List[Record]]:
    service = StorageService(max_storage_limit=max_limit)
    records = generate_records(n, "2021-10-03")
    for date, user in records:
        service.add_record(convert_to_date_str(date), user)

    from_date = convert_to_date_object(from_date_str)
    to_date = convert_to_date_object(to_date_str)
    return service.get_records_interval(from_date, to_date), records


def test_get_records_interval_empty():
    assert query_get_records_interval(10, "1861-10-03", "1990-10-03")[0] == []


def test_get_records_interval_bad_date():
    pytest.raises(BadDateException, query_get_records_interval, 10, "1990-12-04", "1990-10-03")


def test_get_records_interval_equal_bounds():
    ans, records = query_get_records_interval(10, "2021-10-03", "2021-10-03")
    assert ans == records[:1]


def test_get_records_interval_simple():
    ans, records = query_get_records_interval(10, "2021-10-03", "2021-10-09")
    assert ans == records[:7]


def test_get_records_interval_over_max_limit():
    ans, records = query_get_records_interval(10, "2021-10-03", "2021-10-12", 1)
    assert ans == [records[-1]]
