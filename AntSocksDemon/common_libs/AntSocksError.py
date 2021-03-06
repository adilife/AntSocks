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


class AntSockServerConnectionRefused(Exception):
    def __init__(self):
        super().__init__(self)
        self.err = 'AntSocks Server Connection Refused!'

    def __str__(self):
        return self.err


class AntSockServerHandshakeRefused(Exception):
    def __str__(self):
        return 'AntSocks Server handshake refused!'


class AntSockServerHandshakeError(Exception):
    def __str__(self):
        return 'AntSocks Server handshake error!'


class Error(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err
