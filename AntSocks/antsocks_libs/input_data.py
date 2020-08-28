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


def cmd_input():
    while True:
        cmd = input("(quit退出)>>").strip()
        in_porcess = True
        if len(cmd) == 0:
            continue
        elif cmd.upper() == 'QUIT':
            in_porcess = False
            break
        else:
            break
    return cmd, in_porcess


def cmd_buffed_input():
    buffer = []
    while True:
        cmd = input("(EOF结束输入，quit退出)>>").strip()
        in_porcess = True
        if len(cmd) == 0:
            continue
        elif cmd.upper() == 'EOF':
            break
        elif cmd.upper() == 'QUIT':
            in_porcess = False
            break
        else:
            buffer.append(cmd)
    return str(buffer), in_porcess

