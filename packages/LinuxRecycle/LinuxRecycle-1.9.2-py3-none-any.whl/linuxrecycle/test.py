#!/usr/bin/env python3
# encoding: utf-8
# coding style: pep8
# ====================================================
#   Copyright (C)2020 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : test.py
#   Create Time   : 2020-07-05 13:47
#   Last Modified : 2020-07-05 13:47
#   Describe      :
#
# ====================================================
import os
afiel = "/etc/passwd/ad/d"
ll = afiel[1:].split('/')
print(os.path.expanduser("~"))
