# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月06日 19点40分
@Function: 把author信息转化为csv
"""
import pandas as pd

from Reader.AuthorReader import read_author
from utils import *

author_csv_path = get_author_csv_path()
author_affiliation_csv_path = get_author_affiliation_csv_path()
author_interest_csv_path = get_author_interest_csv_path()

author_set = set()
author_list = []
affiliations_list = []
cnt = 0


@timer("读取本地作者信息")
def read_author_info():
    global cnt
    for author in read_author():
        if author.name.strip() == "" or author.name in author_set:
            continue
        author_set.add(author.name)
        author_list.append(author.to_dict())
        for affiliation in author.get_affiliations_name_list():
            if affiliation.strip() == "":
                continue
            affiliations_list.append({"author": author.name, "affiliation": affiliation})

        cnt += 1
        if cnt % 1000 == 0:
            print(f"已完成{cnt}")


@timer("写入csv")
def write_csv():
    pd.DataFrame(author_list).to_csv(author_csv_path, index=False, sep=';')
    pd.DataFrame(affiliations_list).to_csv(author_affiliation_csv_path, index=False, sep=';')
    # 不再把interest作为节点
    # pd.DataFrame(interests_list).to_csv(author_interest_csv_path, index=False, sep=';')


def main():
    read_author_info()
    write_csv()
