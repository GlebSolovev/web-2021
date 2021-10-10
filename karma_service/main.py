import grpc
from concurrent import futures

from karma_service import karma_pb2_grpc
from karma_service.karma_service import KarmaService

MAX_SERVICE_WORKERS = 3


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_SERVICE_WORKERS))
    karma_pb2_grpc.add_KarmaServicer_to_server(
        KarmaService(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
