import grpc
from concurrent import futures

from users_service import users_pb2_grpc
from users_service.users_service import UsersService

MAX_SERVICE_WORKERS = 3


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_SERVICE_WORKERS))
    users_pb2_grpc.add_UsersServicer_to_server(
        UsersService(), server
    )
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
