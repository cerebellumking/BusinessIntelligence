# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 22点47分
@Function: 读Author数据
"""
import fileinput

from Modal.Author import Author
from utils import get_author_path


def read_author():
    path = get_author_path()
    author = None
    for line in fileinput.input(path, openhook=fileinput.hook_encoded("utf-8")):
        if line.strip() == "" or line.strip()[0] != "#":
            if author is not None:
                yield author
                author = None
            else:
                continue

        if author is None:
            author = Author()
        label = line[:line.find(" ")].strip()
        value = line[line.find(" ") + 1:].strip()
        if label == "#index":
            author.set_index(int(value))
        elif label == "#n":
            author.set_name(value)
        elif label == "#a" and value.strip() != "":
            author.set_affiliations(value.split(";"))
        elif label == "#pc":
            author.set_pc(int(value))
        elif label == "#cn":
            author.set_cn(int(value))
        elif label == "#hi":
            author.set_hi(int(value))
        elif label == "#pi":
            author.set_pi(float(value))
        elif label == "#upi":
            author.set_upi(float(value))
        elif label == "#t" and value.strip() != "":
            author.set_interests(value.split(";"))
