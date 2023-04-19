# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月15日 19点48分
@Function: 读Coauthor文件
"""
import fileinput

from Modal.Collaboration import Collaboration
from utils import get_coauthor_path


def read_coauthor():
    path = get_coauthor_path()
    collaboration = None
    for line in fileinput.input(path, openhook=fileinput.hook_encoded("utf-8")):
        if line.strip() == "" or line.strip()[0] != "#":
            continue
        value = line[1:].strip() \
            .replace("\\", "") \
            .replace("\"", "") \
            .replace("\'", "").split("\t")

        if len(value) != 3:
            continue

        yield Collaboration(name1=value[0].strip(), name2=value[1].strip(), count=int(value[2]))
