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
import configparser
import os, sys

# import AntSocks module
from client_para import *


CONF_FILE_EXIST = False
CONF_FILE_ACCESSIBLE = False

TCP_SERVER_IP = DEFAULT_TCP_SERVER_PORT  # type str
TCP_SERVER_PORT = DEFAULT_TCP_SERVER_IP  # type int
TCP_CONN = DEFAULT_TCP_CONN  # type boolen

TCP_LISTEN_IP = DEFAULT_TCP_LISTEN_IP  # type str
TCP_LISTEN_PORT = DEFAULT_TCP_LISTEN_PORT  # type int
TCP_LISTENER = DEFAULT_TCP_LISTENER  # type boolen

CLIENT_NAME = DEFAULT_CLIENT_NAME  # type str

ENCRYPT_KEY = DEFAULT_ENCRYPT_KEY  # type str


# 判断是否存在配置文件
def __check_conf_file():
    # check file accessible.
    global CONF_FILE_EXIST
    global CONF_FILE_ACCESSIBLE
    if os.access(DEFAULT_CONF_FILE_NAME, os.F_OK):
        CONF_FILE_EXIST = True
        if os.access(DEFAULT_CONF_FILE_NAME, os.R_OK) and os.access(DEFAULT_CONF_FILE_NAME, os.W_OK):
            CONF_FILE_ACCESSIBLE = True
        else:
            logging.critical('Conf file is NOT accessible!')
            sys.exit(2)
    else:
        pass


# 存在配置文件，读取配置
def __read_conf_file():
    cp = configparser.ConfigParser()
    cp.read(DEFAULT_CONF_FILE_NAME)

    # 处理Remote Server参数
    global TCP_SERVER_IP # type string
    global TCP_SERVER_PORT # type int
    global TCP_CONN # type boolen

    remote_server = 'Remote_Server'
    TCP_CONN = cp.getboolean(remote_server, 'TCP_CONN')
    TCP_SERVER_IP = cp.get(remote_server, 'TCP_SERVER_IP')
    TCP_SERVER_PORT = cp.getint(remote_server, 'TCP_SERVER_PORT')

    # 处理Local_TCP_Listener参数
    global TCP_LISTEN_IP  # type string
    global TCP_LISTEN_PORT  # type int
    global TCP_LISTENER  # type boolen

    tcp_listener = 'Local_TCP_Listener'
    TCP_LISTENER = cp.getboolean(tcp_listener, 'TCP_LISTENER')
    TCP_LISTEN_IP = cp.get(tcp_listener, 'TCP_LISTEN_IP')
    TCP_LISTEN_PORT = cp.getint(tcp_listener, 'TCP_LISTEN_PORT')

    # 处理client name参数
    global CLIENT_NAME # type string

    cn = 'Client_Name'
    CLIENT_NAME = cp.get(cn, 'CLIENT_NAME')

    # 处理Encrypt参数
    global ENCRYPT_KEY

    ek = 'Encrypt'
    ENCRYPT_KEY = cp.get(ek, 'ENCRYPT_KEY')


# 不存在配置文件，初始化配置文件，初始化配置
def __create_conf_file():
    cp = configparser.ConfigParser()

    # 处理Remote Server参数
    remote_server = 'Remote_Server'
    cp.add_section(remote_server)
    cp.set(remote_server, 'TCP_CONN', str(TCP_CONN))
    cp.set(remote_server, 'TCP_SERVER_IP', TCP_SERVER_IP)
    cp.set(remote_server, 'TCP_SERVER_PORT', str(TCP_SERVER_PORT))

    # 处理Local_TCP_Listener参数
    tcp_listener = 'Local_TCP_Listener'
    cp.add_section(tcp_listener)
    cp.set(tcp_listener, 'TCP_LISTENER', str(TCP_LISTENER))
    cp.set(tcp_listener, 'TCP_LISTEN_IP', TCP_LISTEN_IP)
    cp.set(tcp_listener, 'TCP_LISTEN_PORT', str(TCP_LISTEN_PORT))

    # 处理client name参数
    cn = 'Client_Name'
    cp.add_section(cn)
    cp.set(cn, 'CLIENT_NAME', CLIENT_NAME)

    # 处理Encrypt参数
    ek = 'Encrypt'
    cp.add_section(ek)
    cp.set(cn, 'ENCRYPT_KEY', ENCRYPT_KEY)

    # 写入配置文件
    f = open(DEFAULT_CONF_FILE_NAME, 'w')
    try:
        cp.write(f)
    except Exception as e:
        logging.critical('Cannot create conf file! ' + str(e))
        raise


#  执行
def go():
    __check_conf_file()
    if CONF_FILE_ACCESSIBLE:
        __read_conf_file()

    if not CONF_FILE_EXIST:
        __create_conf_file()



