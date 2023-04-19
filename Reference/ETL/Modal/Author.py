# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点03分
@Function: 作者
"""
from py2neo import Node, Graph

from Modal.Affiliation import Affiliation
from Modal.Interest import Interest


class Author:
    def __init__(self,
                 index=-1,
                 name="",
                 affiliations=None,
                 pc=0,
                 cn=0,
                 hi=0,
                 pi=0.0,
                 upi=0.0,
                 interests=None
                 ):
        if affiliations is None:
            affiliations = []
        if interests is None:
            interests = []

        self.index = index
        self.name = name
        self.affiliations = [Affiliation(affiliation) for affiliation in affiliations]
        self.pc = pc
        self.cn = cn
        self.hi = hi
        self.pi = pi
        self.upi = upi
        self.interests = [Interest(interest) for interest in interests]

    def set_index(self, index):
        self.index = index

    def set_name(self, name):
        self.name = name

    def set_affiliations(self, affiliations):
        self.affiliations = [Affiliation(affiliation) for affiliation in affiliations]

    def set_interests(self, interests):
        self.interests = [Interest(interest) for interest in interests]

    def set_pc(self, pc):
        self.pc = pc

    def set_cn(self, cn):
        self.cn = cn

    def set_hi(self, hi):
        self.hi = hi

    def set_pi(self, pi):
        self.pi = pi

    def set_upi(self, upi):
        self.upi = upi

    def get_affiliations_list(self):
        return self.affiliations

    def get_affiliations_name_list(self):
        return [a.name for a in self.affiliations]

    def get_interests_list(self):
        return self.interests

    def get_interests_name_list(self):
        return [i.name for i in self.interests]

    def to_string(self):
        return "Author: " + self.name + " " + str(self.index) + " " + str(self.pc) + " " + str(self.cn) + " " + str(
            self.hi) + " " + str(self.pi) + " " + str(self.upi) + " " + str(self.affiliations) + " " + str(
            self.interests)

    def to_dict(self):
        # 现在把interest作为属性
        interest_str = ""
        cnt = 0
        for interest in self.interests:
            if cnt > 0:
                interest_str += "," + interest.name
            cnt += 1
        return {
            "index": self.index,
            "name": self.name,
            "pc": self.pc,
            "cn": self.cn,
            "hi": self.hi,
            "pi": self.pi,
            "upi": self.upi,
            "interest": interest_str
        }
