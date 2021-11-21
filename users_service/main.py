import grpc
from concurrent import futures

from users_service import users_pb2_grpc
from users_service.users_service import UsersService
from utils.constants import Constants


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=Constants.MAX_USERS_SERVERS_WORKERS))
    users_pb2_grpc.add_UsersServicer_to_server(
        UsersService(), server
    )
    server.add_insecure_port("[::]:" + str(Constants.USERS_SERVICE_PORT))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
