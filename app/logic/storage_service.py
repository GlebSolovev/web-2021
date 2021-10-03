import heapq
from datetime import datetime, timedelta

from typing import List, Tuple, NoReturn

from app.logic.constants import Constants
from app.logic.exceptions import BadDateException
from app.logic.user import User

Record = Tuple[datetime.date, User]


def convert_to_date_object(date_str: str) -> datetime.date:
    return datetime.strptime(date_str, Constants.DATE_FORMAT).date()


def convert_to_date_str(date: datetime.date) -> str:
    return date.strftime(Constants.DATE_FORMAT)


class StorageService:

    def __init__(self, max_storage_limit=365):
        self.max_storage_limit = max_storage_limit
        self.storage = {}
        self.dates = []
        heapq.heapify(self.dates)

    def add_record(self, date_str: str, happy_user: User) -> NoReturn:
        date = convert_to_date_object(date_str)

        if date in self.storage:
            self.storage[date] = happy_user
            return

        if len(self.storage) == self.max_storage_limit:
            oldest_date = heapq.heappop(self.dates)
            self.storage.pop(oldest_date)

        self.storage[date] = happy_user
        heapq.heappush(self.dates, date)

    def get_record(self, date: datetime.date) -> Record:
        if date not in self.storage:
            raise BadDateException
        return date, self.storage[date]

    def get_records_interval(self, from_date: datetime.date, to_date: datetime.date) -> List[Record]:
        date = from_date
        delta = to_date - from_date
        if delta < timedelta(0):
            raise BadDateException
        res = []
        for i in range(delta.days + 1):
            if date in self.storage:
                res.append((date, self.storage[date]))
            date += timedelta(days=1)
        return res
