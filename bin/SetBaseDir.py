# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 21:27
# @Author  : Abner
# @File    : SetBaseDir.py
# @Software: PyCharm

import sys, os

def set_env_path():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    return BASE_DIR

BASE_DIR = set_env_path()
