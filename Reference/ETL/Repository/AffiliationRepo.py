# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点47分
@Function: 请描述这个py文件的作用
"""
from Modal.Affiliation import Affiliation
from py2neo import Graph, NodeMatcher, Node


class AffiliationRepo:
    label = "Affiliation"

    def __init__(self):
        pass

    @staticmethod
    def create_affiliation_check(graph: Graph, affiliation: Affiliation):
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match(AffiliationRepo.label, name=affiliation.name).first()
        if node is None:
            node = AffiliationRepo.create_affiliation(graph, affiliation)
        return node

    @staticmethod
    def create_affiliation(graph: Graph, affiliation: Affiliation):
        node = Node(AffiliationRepo.label, name=affiliation.name)
        graph.create(node)
        graph.push(node)
        return node

    @staticmethod
    def get_affiliation_by_name(graph: Graph, name: str) -> Node:
        node_matcher = NodeMatcher(graph)
        return node_matcher.match(AffiliationRepo.label, name=name).first()

    @staticmethod
    def get_all_affiliation_dict(graph: Graph) -> dict:
        cql = "match (n:Affiliation) return (n);"
        nodes = [x["n"] for x in graph.run(cql).data()]
        return {x["name"]: x for x in nodes}

    @staticmethod
    def get_all_affiliation_name(graph: Graph) -> set:
        cql = "match (n:Affiliation) return (n.name);"
        return set(x["(n.name)"] for x in graph.run(cql).data())

    @staticmethod
    def to_neo4j_node(affiliation: Affiliation):
        return Node(AffiliationRepo.label, **affiliation.to_dict())
