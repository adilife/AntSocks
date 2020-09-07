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


# import common module
import sys
import socket
import base64
from Crypto import Random

# import antsocks module
from common_libs import encrypt_data, struct_data
from antsocks_libs import conf_file
from common_libs.AntSocksError import *
from client_para import *

# ----读取配置文件
conf_file.go()
# 处理TCP LISTENER参数
TCP_CONN = conf_file.TCP_CONN
TCP_SERVER_IP = conf_file.TCP_SERVER_IP
TCP_SERVER_PORT = conf_file.TCP_SERVER_PORT
# 处理CLIENT_NAME参数
CLIENT_NAME = conf_file.CLIENT_NAME
# 处理ENCRYPT_KEY参数
ENCRYPT_KEY = conf_file.ENCRYPT_KEY


class TcpSender(object):
    def __init__(self):
        self.leads = 'AntComesLetsFigt'.encode('utf-8')
        self.tail = 'Tail'.encode('utf-8')
        self.client_name = CLIENT_NAME
        self.iv = b''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
        except socket.error:
            # Server connection refused
            raise AntSockServerConnectionRefused
        self.server_id = ''
        self.__hand_shake()

    def settimeout(self, timeout):
        self.client.settimeout(timeout)

    def fileno(self):
        return self.client.fileno()

    def close(self):
        self.client.close()

    def __del__(self):
        self.close()

    def send_data(self, data):  # data type bytes
        o_length = len(data)
        body = struct_data.pack_body(data, self.tail)
        encrypted_body = encrypt_data.encrypt_bin(body, ENCRYPT_KEY, self.iv)
        length = struct_data.pack_number(len(encrypted_body))
        chunk = length + encrypted_body
        self.client.sendall(chunk)
        return o_length

    def receive_data(self):
        # read length of data
        try:
            # length = self.client.recv(4)
            r_len = bytearray(2)
            if self.client.recv_into(r_len, 2) != 2:
                self.client.close()
                return b''
            length = struct_data.unpack_number(r_len)
        except ConnectionResetError:
            self.client.close()
            return b''
        except OSError:
            self.client.close()
            return b''
        # read data
        try:
            # data = self.client.recv(length)
            data = bytearray(length)
            view = memoryview(data)
            self.client.settimeout(5)
            while length > 0:
                nbytes = self.client.recv_into(view, length)
                if nbytes == 0:
                    self.client.close()
                    return b''
                view = view[nbytes:]
                length -= nbytes
        except ConnectionResetError:
            self.client.close()
            return b''
        except OSError:
            self.client.close()
            return b''
        encrypted_body = bytes(data)
        body = encrypt_data.decrypt_bin(encrypted_body, ENCRYPT_KEY, self.iv)
        origin_data, tail = struct_data.unpack_body(body)
        if self.tail != tail:
            self.client.close()
            return b''
        return origin_data

    def __hand_shake(self):
        # Send handshake to server, include client_id and AES iv, 64 bits
        bs = 16  # AES.block_size is 16 by default
        self.iv = Random.new().read(bs)
        header = str(base64.encodebytes(struct_data.pack_header(self.leads, self.client_name)), encoding='utf-8')
        encrypt_header = encrypt_data.encrypt(header, ENCRYPT_KEY, self.iv)
        data = struct_data.pack_iv(encrypt_header, self.iv)
        self.client.sendall(data)

        # Recive handshake reply from server, include server_id
        length = 48
        # header = self.client.recv(48)
        try:
            header = bytearray(length)
            view = memoryview(header)
            self.client.settimeout(1)
            while length > 0:
                nbytes = self.client.recv_into(view, length)
                if nbytes == 0:
                    header = b''
                    break
                view = view[nbytes:]
                length -= nbytes
        except ConnectionResetError:
            header = b''
        except OSError:
            header = b''

        if not header:
            self.client.close()
            raise AntSockServerHandshakeRefused
        header = encrypt_data.decrypt(bytes(header), ENCRYPT_KEY, self.iv)
        header = base64.decodebytes(header.encode(encoding='utf-8'))
        header = struct_data.unpack_header(header)
        if self.leads != header[0]:
            self.client.close()
            raise AntSockServerHandshakeError
        self.server_id = self.__get_id(header[1])
        # print('Connected to server {}.'.format(self.server_id))

    @staticmethod
    def __get_id(data):
        return str(data.decode('utf-8')).strip(b'\x00'.decode('utf-8'))
