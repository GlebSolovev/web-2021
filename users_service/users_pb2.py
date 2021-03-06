# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: users.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import utils.utils_pb2 as utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='users.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0busers.proto\x1a\x0butils.proto\"G\n\x07NewUser\x12\x0f\n\x07\x62\x61nk_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04wish\x18\x04 \x01(\t\"Q\n\x04User\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0f\n\x07\x62\x61nk_id\x18\x02 \x01(\x05\x12\x0f\n\x07user_id\x18\x03 \x01(\x05\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0c\n\x04wish\x18\x05 \x01(\t\"%\n\x12GetUserByIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"\"\n\x13GetUserByKeyRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"H\n\x0fGetUserResponse\x12\x13\n\x04user\x18\x01 \x01(\x0b\x32\x05.User\x12 \n\x06status\x18\x02 \x01(\x0e\x32\x10.OperationStatus\"/\n\x11\x41\x64\x64NewUserRequest\x12\x1a\n\x08new_user\x18\x01 \x01(\x0b\x32\x08.NewUser\"C\n\x12\x41\x64\x64NewUserResponse\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x06status\x18\x02 \x01(\x0e\x32\x10.OperationStatus2\xac\x01\n\x05Users\x12\x34\n\x0bGetUserById\x12\x13.GetUserByIdRequest\x1a\x10.GetUserResponse\x12\x36\n\x0cGetUserByKey\x12\x14.GetUserByKeyRequest\x1a\x10.GetUserResponse\x12\x35\n\nAddNewUser\x12\x12.AddNewUserRequest\x1a\x13.AddNewUserResponseb\x06proto3'
  ,
  dependencies=[utils__pb2.DESCRIPTOR,])




_NEWUSER = _descriptor.Descriptor(
  name='NewUser',
  full_name='NewUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bank_id', full_name='NewUser.bank_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='NewUser.user_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='NewUser.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wish', full_name='NewUser.wish', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=99,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='User.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bank_id', full_name='User.bank_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='User.user_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='User.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wish', full_name='User.wish', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=182,
)


_GETUSERBYIDREQUEST = _descriptor.Descriptor(
  name='GetUserByIdRequest',
  full_name='GetUserByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='GetUserByIdRequest.user_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=221,
)


_GETUSERBYKEYREQUEST = _descriptor.Descriptor(
  name='GetUserByKeyRequest',
  full_name='GetUserByKeyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='GetUserByKeyRequest.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=257,
)


_GETUSERRESPONSE = _descriptor.Descriptor(
  name='GetUserResponse',
  full_name='GetUserResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user', full_name='GetUserResponse.user', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='GetUserResponse.status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=331,
)


_ADDNEWUSERREQUEST = _descriptor.Descriptor(
  name='AddNewUserRequest',
  full_name='AddNewUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='new_user', full_name='AddNewUserRequest.new_user', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=333,
  serialized_end=380,
)


_ADDNEWUSERRESPONSE = _descriptor.Descriptor(
  name='AddNewUserResponse',
  full_name='AddNewUserResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='AddNewUserResponse.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='AddNewUserResponse.status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=382,
  serialized_end=449,
)

_GETUSERRESPONSE.fields_by_name['user'].message_type = _USER
_GETUSERRESPONSE.fields_by_name['status'].enum_type = utils__pb2._OPERATIONSTATUS
_ADDNEWUSERREQUEST.fields_by_name['new_user'].message_type = _NEWUSER
_ADDNEWUSERRESPONSE.fields_by_name['status'].enum_type = utils__pb2._OPERATIONSTATUS
DESCRIPTOR.message_types_by_name['NewUser'] = _NEWUSER
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['GetUserByIdRequest'] = _GETUSERBYIDREQUEST
DESCRIPTOR.message_types_by_name['GetUserByKeyRequest'] = _GETUSERBYKEYREQUEST
DESCRIPTOR.message_types_by_name['GetUserResponse'] = _GETUSERRESPONSE
DESCRIPTOR.message_types_by_name['AddNewUserRequest'] = _ADDNEWUSERREQUEST
DESCRIPTOR.message_types_by_name['AddNewUserResponse'] = _ADDNEWUSERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NewUser = _reflection.GeneratedProtocolMessageType('NewUser', (_message.Message,), {
  'DESCRIPTOR' : _NEWUSER,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:NewUser)
  })
_sym_db.RegisterMessage(NewUser)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:User)
  })
_sym_db.RegisterMessage(User)

GetUserByIdRequest = _reflection.GeneratedProtocolMessageType('GetUserByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERBYIDREQUEST,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:GetUserByIdRequest)
  })
_sym_db.RegisterMessage(GetUserByIdRequest)

GetUserByKeyRequest = _reflection.GeneratedProtocolMessageType('GetUserByKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERBYKEYREQUEST,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:GetUserByKeyRequest)
  })
_sym_db.RegisterMessage(GetUserByKeyRequest)

GetUserResponse = _reflection.GeneratedProtocolMessageType('GetUserResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERRESPONSE,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:GetUserResponse)
  })
_sym_db.RegisterMessage(GetUserResponse)

AddNewUserRequest = _reflection.GeneratedProtocolMessageType('AddNewUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDNEWUSERREQUEST,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:AddNewUserRequest)
  })
_sym_db.RegisterMessage(AddNewUserRequest)

AddNewUserResponse = _reflection.GeneratedProtocolMessageType('AddNewUserResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADDNEWUSERRESPONSE,
  '__module__' : 'users_pb2'
  # @@protoc_insertion_point(class_scope:AddNewUserResponse)
  })
_sym_db.RegisterMessage(AddNewUserResponse)



_USERS = _descriptor.ServiceDescriptor(
  name='Users',
  full_name='Users',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=452,
  serialized_end=624,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetUserById',
    full_name='Users.GetUserById',
    index=0,
    containing_service=None,
    input_type=_GETUSERBYIDREQUEST,
    output_type=_GETUSERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUserByKey',
    full_name='Users.GetUserByKey',
    index=1,
    containing_service=None,
    input_type=_GETUSERBYKEYREQUEST,
    output_type=_GETUSERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AddNewUser',
    full_name='Users.AddNewUser',
    index=2,
    containing_service=None,
    input_type=_ADDNEWUSERREQUEST,
    output_type=_ADDNEWUSERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERS)

DESCRIPTOR.services_by_name['Users'] = _USERS

# @@protoc_insertion_point(module_scope)
