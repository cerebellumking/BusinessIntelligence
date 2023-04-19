# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月15日 19点47分
@Function: 把协作关系转化为csv文件
"""
import pandas as pd

from Reader.CoauthorReader import read_coauthor
from utils import get_coauthor_csv_path, timer

coauthor_path = get_coauthor_csv_path()

collaboration_list = []


@timer("读取协作关系")
def read_coauthor_data():
    cnt = 0
    for collaboration in read_coauthor():
        if len(collaboration.name1.strip()) == 0 \
                or len(collaboration.name2.strip()) == 0 \
                or collaboration.count is None:
            continue
        collaboration_list.append(collaboration.to_dict())

        cnt += 1
        if cnt % 100 == 0:
            print(f"已读取{cnt}条数据")


@timer("写入csv文件")
def write_csv():
    pd.DataFrame(collaboration_list).to_csv(coauthor_path, index=False, sep=';')


def main():
    read_coauthor_data()
    write_csv()
