# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import users_pb2 as users__pb2


class UsersStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUserById = channel.unary_unary(
                '/Users/GetUserById',
                request_serializer=users__pb2.GetUserByIdRequest.SerializeToString,
                response_deserializer=users__pb2.GetUserResponse.FromString,
                )
        self.GetUserByKey = channel.unary_unary(
                '/Users/GetUserByKey',
                request_serializer=users__pb2.GetUserByKeyRequest.SerializeToString,
                response_deserializer=users__pb2.GetUserResponse.FromString,
                )
        self.AddNewUser = channel.unary_unary(
                '/Users/AddNewUser',
                request_serializer=users__pb2.AddNewUserRequest.SerializeToString,
                response_deserializer=users__pb2.AddNewUserResponse.FromString,
                )


class UsersServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUserById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserByKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddNewUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UsersServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUserById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserById,
                    request_deserializer=users__pb2.GetUserByIdRequest.FromString,
                    response_serializer=users__pb2.GetUserResponse.SerializeToString,
            ),
            'GetUserByKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserByKey,
                    request_deserializer=users__pb2.GetUserByKeyRequest.FromString,
                    response_serializer=users__pb2.GetUserResponse.SerializeToString,
            ),
            'AddNewUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddNewUser,
                    request_deserializer=users__pb2.AddNewUserRequest.FromString,
                    response_serializer=users__pb2.AddNewUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Users', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Users(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUserById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/GetUserById',
            users__pb2.GetUserByIdRequest.SerializeToString,
            users__pb2.GetUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUserByKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/GetUserByKey',
            users__pb2.GetUserByKeyRequest.SerializeToString,
            users__pb2.GetUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddNewUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/AddNewUser',
            users__pb2.AddNewUserRequest.SerializeToString,
            users__pb2.AddNewUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)