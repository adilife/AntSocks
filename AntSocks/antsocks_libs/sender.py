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
        self.client_name = CLIENT_NAME
        self.data = b''
        self.iv = b''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
        except socket.error:
            # Server connection refused
            logging.critical('AntSocks Server Connection Refused!')
            raise AntSockServerRefusedConnection
        self.server_id = ''
        self.__hand_shake()

    def settimeout(self, timeout):
        self.client.settimeout(timeout)

    def fileno(self):
        return self.client.fileno()

    def close(self):
        self.client.close()

    def __gen_header(self):
        begin = 'AntComesLetsFigt'.encode('utf-8')
        identity = self.client_name[:16].encode('utf-8')
        return struct_data.pack_data(begin, identity)

    def __del__(self):
        self.close()

    def send_data(self, data):  # data type bytes
        o_length = len(data)
        data = encrypt_data.encrypt_bin(data, ENCRYPT_KEY, self.iv)
        length = struct_data.pack_number(len(data))
        data = length + data
        self.client.sendall(data)
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
        data = bytes(data)
        data = encrypt_data.decrypt_bin(data, ENCRYPT_KEY, self.iv)
        self.data = data
        return data

    def __pack_iv(self, data):
        return data[:2] + self.iv + data[2:]

    def __hand_shake(self):
        # Send handshake to server, include client_id and AES iv, 64 bits
        bs = 16  # AES.block_size is 16 by default
        self.iv = Random.new().read(bs)
        header = str(base64.encodebytes(self.__gen_header()), encoding='utf-8')
        encrypt_header = encrypt_data.encrypt(header, ENCRYPT_KEY, self.iv)
        data = self.__pack_iv(encrypt_header)
        self.client.sendall(data)

        # Recive handshake reply from server, include server_id
        header = self.client.recv(48)
        if not header:
            logging.critical('AntSocks Server handshake refused!')
            sys.exit(1)
        header = encrypt_data.decrypt(header, ENCRYPT_KEY, self.iv)
        header = base64.decodebytes(header.encode(encoding='utf-8'))
        header = struct_data.unpack_data(header)
        self.server_id = str(header[1].decode('utf-8')).strip(b'\x00'.decode('utf-8'))
        # print('Connected to server {}.'.format(self.server_id))



