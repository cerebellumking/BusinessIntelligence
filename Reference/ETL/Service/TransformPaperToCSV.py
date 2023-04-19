# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月07日 21点19分
@Function: 请描述这个py文件的作用
"""
import pandas as pd

from Reader.PaperReader import read_paper
from utils import *

paper_path = get_paper_csv_path()
paper_write_path = get_paper_write_csv_path()
paper_participate_path = get_paper_participate_csv_path()
paper_cite_path = get_paper_cite_csv_path()
paper_publication_path = get_paper_publication_csv_path()

paper_index_set = set()
paper_list = []
paper_write_list = []
paper_participate_list = []
paper_cite_list = []
paper_publication_list = []
cnt = 0


@timer("读取paper数据")
def read_paper_data():
    global cnt
    for paper in read_paper():
        if paper.index == -1 or paper.index in paper_index_set:
            continue
        paper_index_set.add(paper.index)
        paper_list.append(paper.to_dict())
        for write_relation in paper.get_write_relations():
            paper_write_list.append(write_relation.to_dict())
        for participate_relation in paper.get_participate_relations():
            paper_participate_list.append(participate_relation.to_dict())
        for cite_relation in paper.get_cite_relations():
            paper_cite_list.append(cite_relation.to_dict())
        for publication in paper.get_publication_relations():
            paper_publication_list.append(publication.to_dict())

        cnt += 1
        if cnt % 1000 == 0:
            print(f"已完成{cnt}")


@timer("写入csv")
def write_csv():
    pd.DataFrame(paper_list).to_csv(paper_path, index=False, sep=';')
    pd.DataFrame(paper_write_list).to_csv(paper_write_path, index=False, sep=';')
    pd.DataFrame(paper_cite_list).to_csv(paper_cite_path, index=False, sep=';')
    pd.DataFrame(paper_publication_list).to_csv(paper_publication_path, index=False, sep=';')
    pd.DataFrame(paper_participate_list).to_csv(paper_participate_path, index=False, sep=';')


def main():
    read_paper_data()
    write_csv()
