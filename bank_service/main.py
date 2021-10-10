import grpc
from concurrent import futures

from bank_service import bank_pb2_grpc
from bank_service.bank_service import BankService
from utils.constants import Constants


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=Constants.MAX_BANK_SERVERS_WORKERS))
    bank_pb2_grpc.add_BankServicer_to_server(
        BankService(), server
    )
    server.add_insecure_port("[::]:" + str(Constants.BANK_SERVICE_PORT))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
