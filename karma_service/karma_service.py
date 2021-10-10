from typing import Dict
import numpy as np

from karma_service.karma_pb2 import (
    ModifyKarmaResponse,
    KarmaResponse,
    AddKarmaUserResponse, ChooseUsersResponse,
)
import karma_service.karma_pb2_grpc as karma_pb2_grpc
from utils.utils_pb2 import OperationStatus


class KarmaService(karma_pb2_grpc.KarmaServicer):

    def __init__(self, max_limit: int = 100_000):
        self.max_limit = max_limit
        self.__karma_database: Dict[int, int] = {}

    def ModifyKarma(self, request, context):
        if request.user_id not in self.__karma_database:
            return ModifyKarmaResponse(status=OperationStatus.USER_NOT_FOUND)
        self.__karma_database[request.user_id] += request.delta
        return ModifyKarmaResponse(status=OperationStatus.SUCCESS)

    def GetKarma(self, request, context):
        if request.user_id not in self.__karma_database:
            return KarmaResponse(status=OperationStatus.USER_NOT_FOUND)
        return KarmaResponse(karma=self.__karma_database[request.user_id], status=OperationStatus.SUCCESS)

    def AddUser(self, request, context):
        new_user_id = len(self.__karma_database)
        if len(self.__karma_database) == self.max_limit:
            return AddKarmaUserResponse(status=OperationStatus.STORAGE_IS_FULL)
        self.__karma_database[new_user_id] = request.karma
        return AddKarmaUserResponse(user_id=new_user_id, status=OperationStatus.SUCCESS)

    def ChooseKarmaWeightedRandomUsers(self, request, context):
        forbidden_set = set(request.forbidden_user_ids)
        candidates = [user_id for user_id, karma in self.__karma_database.items()
                      if karma > 0 and user_id not in forbidden_set]
        weights = np.array([self.__karma_database[user_id] for user_id in candidates])
        probabilities = weights / np.sum(weights)
        if len(candidates) == 0:
            return ChooseUsersResponse(status=OperationStatus.USER_NOT_FOUND)
        chosen_user_ids = np.random.choice(candidates, size=request.users_to_choose, replace=False, p=probabilities)
        return ChooseUsersResponse(user_ids=chosen_user_ids.tolist(), status=OperationStatus.SUCCESS)
