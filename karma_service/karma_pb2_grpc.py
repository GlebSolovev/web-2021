# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import karma_pb2 as karma__pb2


class KarmaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ModifyKarma = channel.unary_unary(
                '/Karma/ModifyKarma',
                request_serializer=karma__pb2.ModifyKarmaRequest.SerializeToString,
                response_deserializer=karma__pb2.ModifyKarmaResponse.FromString,
                )
        self.GetKarma = channel.unary_unary(
                '/Karma/GetKarma',
                request_serializer=karma__pb2.KarmaRequest.SerializeToString,
                response_deserializer=karma__pb2.KarmaResponse.FromString,
                )
        self.AddUser = channel.unary_unary(
                '/Karma/AddUser',
                request_serializer=karma__pb2.AddKarmaUserRequest.SerializeToString,
                response_deserializer=karma__pb2.AddKarmaUserResponse.FromString,
                )
        self.ChooseKarmaWeightedRandomUsers = channel.unary_unary(
                '/Karma/ChooseKarmaWeightedRandomUsers',
                request_serializer=karma__pb2.ChooseUsersRequest.SerializeToString,
                response_deserializer=karma__pb2.ChooseUsersResponse.FromString,
                )


class KarmaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ModifyKarma(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetKarma(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChooseKarmaWeightedRandomUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KarmaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ModifyKarma': grpc.unary_unary_rpc_method_handler(
                    servicer.ModifyKarma,
                    request_deserializer=karma__pb2.ModifyKarmaRequest.FromString,
                    response_serializer=karma__pb2.ModifyKarmaResponse.SerializeToString,
            ),
            'GetKarma': grpc.unary_unary_rpc_method_handler(
                    servicer.GetKarma,
                    request_deserializer=karma__pb2.KarmaRequest.FromString,
                    response_serializer=karma__pb2.KarmaResponse.SerializeToString,
            ),
            'AddUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUser,
                    request_deserializer=karma__pb2.AddKarmaUserRequest.FromString,
                    response_serializer=karma__pb2.AddKarmaUserResponse.SerializeToString,
            ),
            'ChooseKarmaWeightedRandomUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.ChooseKarmaWeightedRandomUsers,
                    request_deserializer=karma__pb2.ChooseUsersRequest.FromString,
                    response_serializer=karma__pb2.ChooseUsersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Karma', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Karma(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ModifyKarma(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Karma/ModifyKarma',
            karma__pb2.ModifyKarmaRequest.SerializeToString,
            karma__pb2.ModifyKarmaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetKarma(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Karma/GetKarma',
            karma__pb2.KarmaRequest.SerializeToString,
            karma__pb2.KarmaResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Karma/AddUser',
            karma__pb2.AddKarmaUserRequest.SerializeToString,
            karma__pb2.AddKarmaUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChooseKarmaWeightedRandomUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Karma/ChooseKarmaWeightedRandomUsers',
            karma__pb2.ChooseUsersRequest.SerializeToString,
            karma__pb2.ChooseUsersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)