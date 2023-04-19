# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点21分
@Function: 请描述这个py文件的作用
"""


class Collaboration:
    def __init__(self, name1="", name2="", count=0):
        self.name1 = name1
        self.name2 = name2
        self.count = count

    def to_dict(self):
        return {
            "name1": self.name1,
            "name2": self.name2,
            "count": self.count
        }
