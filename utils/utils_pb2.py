# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='utils.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0butils.proto*s\n\x0fOperationStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x14\n\x10NOT_ENOUGH_COINS\x10\x01\x12\x14\n\x10SELF_TRANSACTION\x10\x02\x12\x12\n\x0eUSER_NOT_FOUND\x10\x03\x12\x13\n\x0fSTORAGE_IS_FULL\x10\x04\x62\x06proto3'
)

_OPERATIONSTATUS = _descriptor.EnumDescriptor(
  name='OperationStatus',
  full_name='OperationStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ENOUGH_COINS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SELF_TRANSACTION', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='USER_NOT_FOUND', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_IS_FULL', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=15,
  serialized_end=130,
)
_sym_db.RegisterEnumDescriptor(_OPERATIONSTATUS)

OperationStatus = enum_type_wrapper.EnumTypeWrapper(_OPERATIONSTATUS)
SUCCESS = 0
NOT_ENOUGH_COINS = 1
SELF_TRANSACTION = 2
USER_NOT_FOUND = 3
STORAGE_IS_FULL = 4


DESCRIPTOR.enum_types_by_name['OperationStatus'] = _OPERATIONSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
