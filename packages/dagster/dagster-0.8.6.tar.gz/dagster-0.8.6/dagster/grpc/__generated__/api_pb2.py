# @generated

# This file was generated by running `python -m dagster.grpc.compile`
# Do not edit this file directly, and do not attempt to recompile it using
# grpc_tools.protoc directly, as several changes must be made to the raw output

# pylint: disable=protected-access

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='api.proto',
    package='api',
    syntax='proto3',
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\tapi.proto\x12\x03\x61pi\"\x1b\n\x0bPingRequest\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t\"\x19\n\tPingReply\x12\x0c\n\x04\x65\x63ho\x18\x01 \x01(\t28\n\nDagsterApi\x12*\n\x04Ping\x12\x10.api.PingRequest\x1a\x0e.api.PingReply\"\x00\x62\x06proto3',
)


_PINGREQUEST = _descriptor.Descriptor(
    name='PingRequest',
    full_name='api.PingRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name='echo',
            full_name='api.PingRequest.echo',
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=18,
    serialized_end=45,
)


_PINGREPLY = _descriptor.Descriptor(
    name='PingReply',
    full_name='api.PingReply',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name='echo',
            full_name='api.PingReply.echo',
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode('utf-8'),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=47,
    serialized_end=72,
)

DESCRIPTOR.message_types_by_name['PingRequest'] = _PINGREQUEST
DESCRIPTOR.message_types_by_name['PingReply'] = _PINGREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PingRequest = _reflection.GeneratedProtocolMessageType(
    'PingRequest',
    (_message.Message,),
    {
        'DESCRIPTOR': _PINGREQUEST,
        '__module__': 'api_pb2'
        # @@protoc_insertion_point(class_scope:api.PingRequest)
    },
)
_sym_db.RegisterMessage(PingRequest)

PingReply = _reflection.GeneratedProtocolMessageType(
    'PingReply',
    (_message.Message,),
    {
        'DESCRIPTOR': _PINGREPLY,
        '__module__': 'api_pb2'
        # @@protoc_insertion_point(class_scope:api.PingReply)
    },
)
_sym_db.RegisterMessage(PingReply)


_DAGSTERAPI = _descriptor.ServiceDescriptor(
    name='DagsterApi',
    full_name='api.DagsterApi',
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=74,
    serialized_end=130,
    methods=[
        _descriptor.MethodDescriptor(
            name='Ping',
            full_name='api.DagsterApi.Ping',
            index=0,
            containing_service=None,
            input_type=_PINGREQUEST,
            output_type=_PINGREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_DAGSTERAPI)

DESCRIPTOR.services_by_name['DagsterApi'] = _DAGSTERAPI

# @@protoc_insertion_point(module_scope)
