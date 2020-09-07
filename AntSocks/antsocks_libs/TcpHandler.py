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
import time, struct
import sys

# import AntSocks module
from antsocks_libs import sender
from common_libs.AntSocksError import *
from client_para import *


def get_cur_time():
    cur_time = '[%s]' % time.strftime("%Y-%m-%d %X", time.localtime())
    return cur_time


def handle_tcp(sock, remote):
    fdset = [sock, remote]
    while True:
        # 开始 select 监听,对input_list中的服务端server进行监听
        # stdinput, stdoutput, stderr = select(input_list, output_list, input_list)
        r, w, e = select.select(fdset, [], [])
        if sock in r:
            a = sock.recv(1024)
            remote.send_data(a)
            if len(a) == 0:
                break

        if remote in r:
            a = remote.receive_data()
            sock.sendall(a)
            if len(a) == 0:
                break


class Socks5Demon(socketserver.BaseRequestHandler):
    timeout = None

    def __init__(self, request, client_address, server):
        self.cl2sv = ''
        try:
            self.cl2sv = sender.TcpSender()
        except Exception as e:
            logging.critical(str(e))
            sys.exit(1)
        super().__init__(request, client_address, server)

    def __del__(self):
        # self.request.close()
        if self.cl2sv != '':
            self.cl2sv.close()
        pass

    def handle(self):
        if self.timeout is not None:
            self.request.settimeout(self.timeout)
            self.cl2sv.settimeout(self.timeout)

        sock = self.request
        sock_version = 5
        # 协商
        # 从客户端读取并解包两个字节的数据
        header = sock.recv(2)
        if len(header) < 2:
            return
        version, nmethods = struct.unpack("!BB", header)
        # 设置socks5协议，METHODS字段的数目大于0
        assert version == sock_version
        assert nmethods > 0
        # 接受支持的方法
        methods = self.get_available_methods(nmethods)
        # 无需认证
        if 0 not in set(methods):
            return
        # 发送协商响应数据包
        sock.sendall(struct.pack("!BB", sock_version, 0))
        # 请求
        req = sock.recv(4)
        if len(req) < 4:
            return
        version, cmd, _, address_type = struct.unpack("!BBBB", req)
        assert version == sock_version
        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(sock.recv(4))
        elif address_type == 3:  # Domain name
            # print('domain mode')
            domain_length = sock.recv(1)[0]
            address = sock.recv(domain_length)
            # address = socket.gethostbyname(address.decode("UTF-8"))  # 将域名转化为IP，这一行可以去掉
        elif address_type == 4:  # IPv6
            # print('ipv6 !!!!!!!!!!!1')
            addr_ip = sock.recv(16)
            address = socket.inet_ntop(socket.AF_INET6, addr_ip)
        else:
            sock.close()
            return
        port = struct.unpack('!H', sock.recv(2))[0]

        # 响应，只支持CONNECT请求
        try:
            if cmd == 1:  # CONNECT
                self.cl2sv.send_data(address.encode('utf-8'))  # send addr
                self.cl2sv.send_data(str(port).encode('utf-8'))  # send port
                remote_status = self.cl2sv.receive_data().decode('utf-8')  # receive status
                if remote_status == 'Connection refused':
                    reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
                    sock.sendall(reply)
                    sock.close()
                    return

                remote_ip = self.cl2sv.receive_data()
                remote_port = self.cl2sv.receive_data()
                if remote_ip == b'' or remote_port == b'':
                    return
                remote_ip = remote_ip.decode('utf-8')
                remote_port = int(remote_port.decode('utf-8'))

            else:
                reply = b"\x05\x07\x00\x01"  # Command not supported
                sock.sendall(reply)
                sock.close()
                return
            addr = struct.unpack("!I", socket.inet_aton(remote_ip))[0]
            port = remote_port
            # reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type, addr, port)
            # 注意：按照标准协议，返回的应该是对应的address_type，但是实际测试发现，当address_type=3，也就是说是域名类型时，
            # 会出现卡死情况，但是将address_type该为1，则不管是IP类型和域名类型都能正常运行
            reply = struct.pack("!BBBBIH", sock_version, 0, 0, 1, addr, port)
        except Exception as err:
            logging.error(str(err))
            # 响应拒绝连接的错误
            reply = self.generate_failed_reply(address_type, 5)
            sock.sendall(reply)
            sock.close()
            return
        sock.sendall(reply)

        if reply[1] == 0 and cmd == 1:
            handle_tcp(sock, self.cl2sv)

        self.cl2sv.close()
        sock.close()

    def get_available_methods(self, n):
        methods = []
        for i in range(0, n):
            methods.append(ord(self.request.recv(1)))
        return methods

    @staticmethod
    def generate_failed_reply(address_type, error_number):
        socks_version = 5
        return struct.pack("!BBBBIH", socks_version, error_number, 0, address_type, 0, 0)

