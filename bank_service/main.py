import grpc
from concurrent import futures

from bank_service import bank_pb2_grpc
from bank_service.bank_service import BankService

MAX_SERVICE_WORKERS = 3


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_SERVICE_WORKERS))
    bank_pb2_grpc.add_BankServicer_to_server(
        BankService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
