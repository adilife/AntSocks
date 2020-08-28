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
import base64


from Crypto.Cipher import AES

# import antsocks module
from antsocks_libs import pkcs7padding


def encrypt(data, password, iv):
    bs = 16  # AES.block_size is 16 by default
    data = pkcs7padding.appendPadding(bs, data)

    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')

    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.encrypt(data)
    return data


def decrypt(data, password, iv):
    bs = 16  # AES.block_size is 16 by default
    if len(data) < bs:
        return data
    # data = data[:2] + data[18:]
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(iv, str):
        iv = iv.encode('utf-8')
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.decrypt(data).decode('utf-8')
    data = pkcs7padding.removePadding(bs, data)
    return data


def encrypt_bin(data, password, iv):
    s = str(base64.encodebytes(data), encoding='utf-8')
    s = encrypt(s, password, iv)
    return s


def decrypt_bin(data, password, iv):
    s = decrypt(data, password, iv)
    s = base64.decodebytes(s.encode(encoding='utf-8'))
    return s


if __name__ == '__main__':
    data = 'd437814d9185a290af20514d9341b710'
    password = '78f40f2c57eee727a4be179049cecf89'  # 16,24,32位长的密码
    iv = '1234567890123456'
    encrypt_data = encrypt(data, password, iv)
    encrypt_data = base64.b64encode(encrypt_data)
    print('encrypt_data:', encrypt_data)

    encrypt_data = base64.b64decode(encrypt_data)
    decrypt_data = decrypt(encrypt_data, password, iv)
    print('decrypt_data:', decrypt_data)



