# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月06日 19点23分
@Function: 为Author添加关系
"""
from py2neo import *
import time

from Reader.AuthorReader import read_author
from Repository.AffiliationRepo import AffiliationRepo
from Repository.AuthorRepo import AuthorRepo
from Repository.InterestRepo import InterestRepo
from utils import *

url, account, password = get_neo4j_info()
graph = Graph(url, auth=(account, password))

create_rel_cnt = 0
create_relations = []


@timer("读取本地作者信息")
def read_author_info():
    global create_rel_cnt, create_relations

    create_rel_cnt = 0
    cnt = 0

    for author in read_author():
        author_node = AuthorRepo.get_author_by_name(graph, author.name)
        if author_node is None:
            continue
        affiliation_nodes = AuthorRepo.get_affiliation_list(graph, author)
        interest_nodes = AuthorRepo.get_interest_list(graph, author)
        for affiliation_node in affiliation_nodes:
            create_relations.append(Relationship(author_node, "Work At", affiliation_node))
            create_relations.append(Relationship(affiliation_node, "HAVE", author_node))
            create_rel_cnt += 1

        for interest_node in interest_nodes:
            create_relations.append(Relationship(author_node, "Interest in", interest_node))
            create_relations.append(Relationship(interest_node, "HAVE", author_node))
            create_rel_cnt += 1

        cnt += 1
        if cnt % 1000 == 0:
            print(f"已完成{cnt}")


batch_size = 100


@timer("批量创建关系")
def create_relationship():
    if create_rel_cnt > 0:
        for i in range(create_rel_cnt // 50 + 1):
            subgraph = Subgraph(relationships=create_relations[i * batch_size: (i + 1) * batch_size])
            graph.create(subgraph)
            print(f"create {(i + 1) * batch_size} relations | total {create_rel_cnt} relationships")
