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
import configparser
import os, sys
# import AntSocks module
from server_para import *


CONF_FILE_EXIST = False
CONF_FILE_ACCESSABLE = False


# 判断是否存在配置文件
def __check_conf_file():
    # check file accessable.
    global CONF_FILE_EXIST
    global CONF_FILE_ACCESSABLE
    if os.access(CONF_FILE_NAME, os.F_OK):
        CONF_FILE_EXIST = True
        if os.access(CONF_FILE_NAME, os.R_OK) and os.access(CONF_FILE_NAME, os.W_OK):
            CONF_FILE_ACCESSABLE = True
        else :
            print ('Conf file is NOT accessable!')
            sys.exit(2)
    else:
        pass


# 存在配置文件，读取配置
def __read_conf_file():
    cp = configparser.ConfigParser()
    cp.read(CONF_FILE_NAME)

    # 处理tcp listener参数
    global TCP_LISTEN_IP  # type string
    global TCP_LISTEN_PORT  # type int
    global TCP_LISTENER  # type boolen

    tcp_listener = 'TCP_Listener'
    TCP_LISTENER = cp.getboolean(tcp_listener, 'TCP_LISTENER')
    TCP_LISTEN_IP = cp.get(tcp_listener, 'TCP_LISTEN_IP')
    TCP_LISTEN_PORT = cp.getint(tcp_listener, 'TCP_LISTEN_PORT')

    # 处理 server参数
    global SERVER_NAME  # type str
    server_para = 'Server'
    SERVER_NAME = cp.get(server_para, 'SERVER_NAME')

    # 处理 encrypt参数
    global ENCRYPT_KEY  # type str
    encrypt_para = 'Encrypt'
    ENCRYPT_KEY = cp.get(encrypt_para, 'ENCRYPT_KEY')


# 不存在配置文件，初始化配置文件，初始化配置
def __creat_conf_file():

    cp = configparser.ConfigParser()

    # 处理tcp listener参数
    global TCP_LISTEN_IP  # type string
    global TCP_LISTEN_PORT  # type int
    global TCP_LISTENER  # type boolen

    tcp_listener = 'TCP_Listener'
    cp.add_section(tcp_listener)
    cp.set(tcp_listener, 'TCP_LISTENER', str(TCP_LISTENER))
    cp.set(tcp_listener, 'TCP_LISTEN_IP', TCP_LISTEN_IP)
    cp.set(tcp_listener, 'TCP_LISTEN_PORT', str(TCP_LISTEN_PORT))

    # 处理 server参数
    global SERVER_NAME  # type str
    server_para = 'Server'
    cp.add_section(server_para)
    cp.set(server_para, 'SERVER_NAME', SERVER_NAME)

    # 处理 encrypt参数
    global ENCRYPT_KEY  # type str
    encrypt_para = 'Encrypt'
    cp.add_section(encrypt_para)
    cp.set(encrypt_para, 'ENCRYPT_KEY', ENCRYPT_KEY)

    # 写配置文件
    f = open(CONF_FILE_NAME, 'w')
    try:
        cp.write(f)
    except:
        print('Cannot create conf file!')
        sys.exit(2)


#  执行
def go():
    __check_conf_file()
    if CONF_FILE_ACCESSABLE:
        __read_conf_file()

    if not CONF_FILE_EXIST:
        __creat_conf_file()
    # print(TCP_LISTEN_IP,TCP_LISTEN_PORT,TCP_LISTENER)

