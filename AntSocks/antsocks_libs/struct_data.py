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

STRUCT_FORMAT = '!16s16s'
N_STRUCT_FORMAT = '!H'


def pack_data(begin,identity):
    s_struct = struct.Struct(STRUCT_FORMAT)
    return s_struct.pack(begin, identity)


def unpack_data(data):
    s_struct = struct.Struct(STRUCT_FORMAT)
    return s_struct.unpack(data)


def pack_number(number):
    n_struct = struct.Struct(N_STRUCT_FORMAT)
    return n_struct.pack(number)


def unpack_number(data):
    n_struct = struct.Struct(N_STRUCT_FORMAT)
    return n_struct.unpack(data)[0]

