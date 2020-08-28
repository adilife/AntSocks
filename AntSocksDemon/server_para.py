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


# default server name
DEFAULT_SERVER_NAME = 'Server1'

# default listener para
DEFAULT_TCP_LISTEN_IP = '127.0.0.1'
DEFAULT_TCP_LISTEN_PORT = 9999
DEFAULT_TCP_LISTENER = True

# default conf file
DEFAULT_CONF_FILE_NAME = 'antsocksd.conf'

# default encrypt key
DEFAULT_ENCRYPT_KEY = '78f41f2c57efa727a4be179049cecf89'


# define logging method
import logging  # 引入logging模块
from server import LOGGING_LEVEL

LOGGING_FORMAT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)  # logging.basicConfig函数对日志的输出格式及方式做相关配置

