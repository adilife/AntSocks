#!/usr/bin/python3
# -*- coding:utf-8 -*-

# Copyright 2020 Ozward Wang
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import struct

HEADER_STRUCT_FORMAT = '!16s16s'
N_STRUCT_FORMAT = '!H'


def pack_number(number):
    n_struct = struct.Struct(N_STRUCT_FORMAT)
    return n_struct.pack(number)


def unpack_number(data):
    n_struct = struct.Struct(N_STRUCT_FORMAT)
    return n_struct.unpack(data)[0]


def pack_header(leads, client_id):
    s_struct = struct.Struct(HEADER_STRUCT_FORMAT)
    if isinstance(client_id, str):
        identity = client_id.encode('utf-8')[:16]
    else:
        identity = client_id[:16]
    return s_struct.pack(leads, identity)


def unpack_header(header):
    s_struct = struct.Struct(HEADER_STRUCT_FORMAT)
    leads, identity = s_struct.unpack(header)
    return leads, identity


def pack_iv(data, iv):
    return data[:2] + iv + data[2:]


def unpack_iv(header):
    data = header[:2] + header[18:]
    iv = header[2:18]
    return iv, data


def pack_body(data, tail):
    return data + tail


def unpack_body(body):
    return body[:-4], body[-4:]



