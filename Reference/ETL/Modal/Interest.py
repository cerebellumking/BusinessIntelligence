# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点14分
@Function: 请描述这个py文件的作用
"""
from py2neo import Node


class Interest:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'name': self.name
        }
