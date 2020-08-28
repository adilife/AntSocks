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
import socketserver, socket, select
import time
import base64
# import AntSocks module
from common_libs import encrypt_data, struct_data
from antsocksd_libs import conf_file
from server_para import *


# ----读取配置文件
conf_file.go()
# 处理TCP LISTENER参数
# 处理ENCRYPT_KEY参数
ENCRYPT_KEY = conf_file.ENCRYPT_KEY
SERVER_NAME = conf_file.SERVER_NAME


def get_cur_time():
    cur_time = '[%s]' % time.strftime("%Y-%m-%d %X", time.localtime())
    return cur_time


class AntTcpHandler(socketserver.BaseRequestHandler):
    timeout = None

    def __init__(self, request, client_address, server):
        self.client_id = ''
        self.data = b''
        self.iv = ''
        self.remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Final target connect by client request.
        self.remote.settimeout(self.timeout)
        super().__init__(request, client_address, server)

    def fileno(self):
        return self.request.fileno()

    def __del__(self):
        self.remote.close()
        self.request.close()

    def handle(self):
        if self.timeout is not None:
            self.remote.settimeout(self.timeout)
        # handshake
        self.__hand_shake()
        # connect to remote target
        is_conn_remote_success = self.__process_conn_remote()
        if not is_conn_remote_success:
            self.request.close()
            self.remote.close()
            return
        # transferring
        self.__process_transfer()
        # close client conns
        logging.debug(get_cur_time(), self.client_address, "连接断开")

    def __process_conn_remote(self):
        # receive ip
        tar_ip = self.receive_cl().decode('utf-8')  # str
        if not tar_ip:
            return False
        tar_port = self.receive_cl().decode('utf-8')  # str
        if not tar_port:
            return False
        tar_status = 'Connection success'.encode('utf-8')  # bin
        # connect to target
        try:
            self.remote.connect((tar_ip, int(tar_port)))
            _tmp_local = self.remote.getsockname()
            _tmp_local_ip = _tmp_local[0].encode('utf-8')
            _tmp_local_port = str(_tmp_local[1]).encode('utf-8')
        except socket.error:
            # Connection refused
            tar_status = 'Connection refused'.encode('utf-8')
            self.reply_cl(tar_status)
            logging.info('From {}, connect to {}:{} FAILED.'.format(self.client_id, tar_ip, tar_port))
            return False

        # send connect result to client
        self.reply_cl(tar_status)

        logging.info('From {}, connect to {}:{} SUCCESS.'.format(self.client_id, tar_ip, tar_port))
        self.reply_cl(_tmp_local_ip)
        self.reply_cl(_tmp_local_port)
        return True

    def __process_transfer(self):
        sock = self
        remote = self.remote
        fdset = [sock, remote]
        while True:
            # 开始 select 监听,对input_list中的服务端server进行监听
            # stdinput, stdoutput, stderr = select(input_list, output_list, input_list)
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                data = sock.receive_cl()
                remote.sendall(data)
                if len(data) == 0:
                    break
            if remote in r:
                data = remote.recv(1024)
                sock.reply_cl(data)
                if len(data) == 0:
                    break
        remote.close()
        sock.close()

    def setup(self):
        logging.debug(get_cur_time(), "before handle,连接建立：", self.client_address)
        pass

    def finish(self):
        logging.debug(get_cur_time(), "finish run  after handle")
        pass

    def __hand_shake(self):
        # receive handshake from client, get client_id and iv
        header = self.request.recv(64)
        if not header:
            # cur_time = get_cur_time()
            # print(cur_time, self.client_address, "HandShake Failed, 连接断开!")
            self.request.close()
            self.remote.close()
            return
        self.iv, header = self.__unpack_iv(header)
        header = encrypt_data.decrypt(header, ENCRYPT_KEY, self.iv)
        header = base64.decodebytes(header.encode(encoding='utf-8'))
        header = struct_data.unpack_data(header)
        self.client_id = header[1].decode('utf-8').strip(b'\x00'.decode('utf-8'))

        # agree client handshake, send replay include server_id, 48 bits
        header = str(base64.encodebytes(self.__gen_header()), encoding='utf-8')
        header = encrypt_data.encrypt(header, ENCRYPT_KEY, self.iv)
        self.request.sendall(header)

        # disagree client handshake, close the request
        # self.request.close()

    @staticmethod
    def __gen_header():
        begin = 'AntComesLetsFigt'.encode('utf-8')
        identity = SERVER_NAME[:16].encode('utf-8')
        return struct_data.pack_data(begin, identity)

    @staticmethod
    def __unpack_iv(header):
        data = header[:2] + header[18:]
        iv = header[2:18]
        return iv, data

    def receive_cl(self):
        """
        Receive data from Antsock Client.
        :return:
        """
        # read length of data
        try:
            # length = self.client.recv(4)
            r_len = bytearray(2)
            if self.request.recv_into(r_len, 2) != 2:
                self.request.close()
                return b''
            length = struct_data.unpack_number(r_len)
        except ConnectionResetError:
            self.request.close()
            return b''
        except OSError:
            self.request.close()
            return b''

        # read data
        try:
            # data = self.client.recv(length)
            data = bytearray(length)
            view = memoryview(data)
            self.request.settimeout(5)
            while length > 0:
                nbytes = self.request.recv_into(view, length)
                if nbytes == 0:
                    self.request.close()
                    return b''
                view = view[nbytes:]
                length -= nbytes
        except ConnectionResetError:
            self.request.close()
            return b''
        except OSError:
            self.request.close()
            return b''

        data = bytes(data)
        data = encrypt_data.decrypt_bin(data, ENCRYPT_KEY, self.iv)
        self.data = data
        return data

    def reply_cl(self, data):
        """
        Send data to Antsock client.
        :param data:
        :return:
        """
        o_length = len(data)
        data = encrypt_data.encrypt_bin(data, ENCRYPT_KEY, self.iv)
        length = struct_data.pack_number(len(data))
        data = length + data
        self.request.sendall(data)
        return o_length

    def close(self):
        self.request.close()





