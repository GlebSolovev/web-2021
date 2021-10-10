from datetime import datetime, timezone

import graphene
from graphene import String, ObjectType, Date, Field, List
from typing import Tuple

from app.logic.exceptions import BadDateException
from app.logic.global_env import GlobalEnv
from app.logic.user import User


class HappyUser(ObjectType):
    name = String(required=True)
    wish = String(required=True)
    # karma = Int(required=True)


class Record(ObjectType):
    date = Date(required=True)
    happy_person = Field(HappyUser, required=True)


def convert_raw_record(raw_record: Tuple[str, User]) -> Record:
    date, user = raw_record
    return Record(date=date, happy_person=HappyUser(name=user.name, wish=user.wish))  # TODO: add karma


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Query(ObjectType):
    record = Field(Record, date=Date(required=True))
    records_interval = List(graphene.NonNull(Record),
                            from_date=Date(default_value=datetime.now(timezone.utc).date(), required=False),
                            to_date=Date(default_value=datetime.now(timezone.utc).date(), required=False))

    def resolve_record(self, info, date):
        try:
            return convert_raw_record(GlobalEnv.handler.storage_service.get_record(date))
        except BadDateException:
            return None

    def resolve_records_interval(self, info, from_date, to_date):
        try:
            raw_records = GlobalEnv.handler.storage_service.get_records_interval(from_date, to_date)
            return [convert_raw_record(raw_record) for raw_record in raw_records]
        except BadDateException:
            return []
