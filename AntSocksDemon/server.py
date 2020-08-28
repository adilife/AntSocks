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


# ----定义logging级别
import logging
LOGGING_LEVEL = logging.INFO  # DEBUG/INFO/WARNING/ERROR/CRITICAL


if __name__ == "__main__":
    import subprocess, os, time
    import socketserver

    # ----创建PID文件
    pid = os.getpid()
    if os.access('antsocksd.pid',os.F_OK):
        subprocess.run('rm -f antsocksd.pid', shell=True)
    with open('antsocksd.pid', 'ta', encoding='utf-8', errors='ignore') as mf:
        mf.write(str(pid))
        mf.close()

    # ----读取配置文件
    from antsocksd_libs import conf_file

    conf_file.go()
    # 处理TCP LISTENER参数
    TCP_LISTENER = conf_file.TCP_LISTENER
    TCP_LISTEN_IP = conf_file.TCP_LISTEN_IP
    TCP_LISTEN_PORT = conf_file.TCP_LISTEN_PORT

    # ----开启TCP监听
    from antsocksd_libs.TcpHandler import AntTcpHandler  # TCP监听程序

    if TCP_LISTENER:
        HOST, PORT = TCP_LISTEN_IP, TCP_LISTEN_PORT
        # server=socketserver.TCPServer((HOST,PORT),AntTcpHandler)  # 单线程
        server = socketserver.ThreadingTCPServer((HOST, PORT), AntTcpHandler)  # 多线程版
        print('[%s]TCP listening: %s:%s ' % (time.strftime("%Y-%m-%d %X", time.localtime()), HOST, PORT))
        # server.timeout = 15
        server.serve_forever()

