# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点12分
@Function: 隶属机构
"""


class Affiliation:
    def __init__(self, name=""):
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }
