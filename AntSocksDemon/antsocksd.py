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
import sys,getopt
import os,subprocess
# import AntSocks module


def main(argv):
    opts = []
    try:
        opts, args = getopt.getopt(argv, "hstq", ["help", "start", "terminal", "quit"])
    except getopt.GetoptError:
        print("wrong args!")
        __help_msg()
        exit()

    # 命令行无参数处理
    if opts == []:
        print("no args...")
        __help_msg()
        exit()

    # 命令行参数处理
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                __help_msg()
                exit()
            elif opt in ("-s", "--start"):
                print("Ant'Socks Demon is running...")
                cmd = 'nohup /usr/bin/python3 -u ./server.py > antsocksd.out 2>&1 &'
                subprocess.run(cmd, shell=True)
            elif opt in ("-t", "--terminal"):
                print("Ant'Socks Demon is running...")
                cmd = '/usr/bin/python3 ./server.py'
                subprocess.run(cmd, shell=True)
            elif opt in ("-q", "--quit"):
                print("Ant'Socks Demon is leaving...")
                with open('antsocksd.pid', 'r', encoding='utf-8', errors='ignore') as mf:
                    pid = int(mf.read())
                    mf.close()
                os.kill(pid, 9)
                os.remove('antsocksd.pid')


def __help_msg():
    helpmsg = '''
    usage antsocksd.py [-h -s -t -q | --help --start --terminal --quit]
    Please use argvs.
    -h|--help       Print help msg.
    -s|--start      Start service.
    -t|--terminal   Keep monitor terminal.
    -q|--quit       Quit service.
    '''
    print(helpmsg)


if __name__=="__main__":
    if sys.platform == 'linux':
        #读取命令行参数
        main(sys.argv[1:])
    else:
        print('Not support this OS!')



