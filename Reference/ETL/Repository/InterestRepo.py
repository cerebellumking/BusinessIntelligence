# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 22点09分
@Function: 请描述这个py文件的作用
"""
from py2neo import Graph, NodeMatcher, Node

from Modal.Interest import Interest


class InterestRepo:
    label = "Interest"

    def __init__(self):
        pass

    @staticmethod
    def create_interest_check(graph: Graph, interest: Interest):
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match(InterestRepo.label, name=interest.name).first()
        if node is None:
            node = InterestRepo.create_interest(graph, interest)
        return node

    @staticmethod
    def create_interest(graph: Graph, interest: Interest):
        node = Node(InterestRepo.label, name=interest.name)
        graph.create(node)
        graph.push(node)
        return node

    @staticmethod
    def get_all_interest_dict(graph: Graph) -> dict:
        cql = "match (n:Interest) return (n);"
        nodes = [x["n"] for x in graph.run(cql).data()]
        return {x["name"]: x for x in nodes}

    @staticmethod
    def get_all_interest_name(graph: Graph) -> set:
        cql = "match (n:Interest) return (n.name);"
        return set(x["(n.name)"] for x in graph.run(cql).data())

    @staticmethod
    def get_interest_by_name(graph: Graph, name: str) -> Node:
        node_matcher = NodeMatcher(graph)
        return node_matcher.match(InterestRepo.label, name=name).first()

    @staticmethod
    def to_neo4j_node(interest: Interest):
        return Node(InterestRepo.label, **interest.to_dict())
