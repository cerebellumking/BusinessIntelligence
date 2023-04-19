# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月07日 21点30分
@Function: 读取论文文件
"""
import fileinput

from Modal.Paper import Paper
from utils import get_paper_path


def read_paper():
    path = get_paper_path()
    paper = None
    for line in fileinput.input(path, openhook=fileinput.hook_encoded("utf-8")):
        if line.strip() == "" or line.strip()[0] != "#":
            if paper is not None:
                yield paper
                paper = None
            else:
                continue

        label = line[:line.find(" ")].strip()
        value = line[line.find(" ") + 1:].strip()\
            .replace("\\", "")\
            .replace("\"", "")\
            .replace("\'", "")
        if value == "":
            continue

        if paper is None:
            paper = Paper()

        if label == "#index":
            paper.set_index(int(value))
        elif label == "#*":
            paper.set_title(value)
        elif label == "#@":
            paper.set_authors(value.split(";"))
        elif label == "#t":
            paper.set_year(int(value))
        elif label == "#c":
            paper.set_venue(value)
        elif label == "#%":
            paper.set_cites(int(value))
        elif label == "#!":
            paper.set_abstract(value)
