# -*- coding: utf-8 -*-
# @Time    : 2018/3/29 10:31
# @Author  : Abner
# @File    : Logger.py
# @Software: PyCharm

import logging
# from aliyun_api.logs import ProjectDir
import os


class Logger(object):

    def __init__(self, modelName, fileLog="dfxkdata-mail-loanbill.log"):
        self.modelName = modelName
        self.fileLog = fileLog

    def getLogger(self):

        #创建一个logging的实例logger
        logger = logging.getLogger(self.modelName)
        #设定全局日志级别为DEBUG
        logger.setLevel(logging.INFO)
        #创建一个屏幕的handler，并且设定级别为DEBUG
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        #创建一个日志文件的handler，并且设定级别为DEBUG
        # pwd = os.getcwd()
        # 当前文件的前两级目录
        # grader_father = os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")

        fh = logging.FileHandler(self.fileLog)
        fh.setLevel(logging.CRITICAL)
        fh.setLevel(logging.ERROR)
        fh.setLevel(logging.INFO)
        fh.setLevel(logging.WARN)
        fh.setLevel(logging.DEBUG)
        #设置日志的格式
        formatter = logging.Formatter("%(asctime)s  %(name)s  %(levelname)s  %(message)s")
        #add formatter to ch and fh
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        #add ch and fh to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger
        #'application' code
        #logger.debug("debug message")
        #logger.info("info message")
        #logger.warn("warn message")
        #logger.error("error message")
        #logger.critical("crititcal message")