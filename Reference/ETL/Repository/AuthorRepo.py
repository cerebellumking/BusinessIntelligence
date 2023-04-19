# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 22点12分
@Function: 请描述这个py文件的作用
"""
from py2neo import Graph, NodeMatcher, Node, Relationship

from Modal.Author import Author
from Repository.AffiliationRepo import AffiliationRepo
from Repository.InterestRepo import InterestRepo


class AuthorRepo:
    label = "Author"

    def __init__(self):
        pass

    @staticmethod
    def create_author_check(graph: Graph, author: Author):
        node = None
        if author.index != -1:
            node = AuthorRepo.get_author_by_id(graph, author.index)
        if node is None:
            node = AuthorRepo.get_author_by_name(graph, author.name)
        if node is None:
            node = AuthorRepo.create_author(graph, author)
        return node

    @staticmethod
    def create_author(graph: Graph, author: Author):
        node = Node(AuthorRepo.label,
                    name=author.name,
                    index=author.index,
                    pc=author.pc,
                    cn=author.cn,
                    hi=author.hi,
                    pi=author.pi,
                    upi=author.upi
                    )
        graph.create(node)
        graph.push(node)
        for affiliation in author.affiliations:
            rel = Relationship(node, "Member of",
                               AffiliationRepo.create_affiliation_check(graph, affiliation))
            graph.create(rel)
            graph.push(rel)
        for interest in author.interests:
            rel = Relationship(node, "Interest", InterestRepo.create_interest_check(graph, interest))
            graph.create(rel)
            graph.push(rel)
        return node

    @staticmethod
    def get_author_by_name(graph: Graph, name: str):
        node_matcher = NodeMatcher(graph)
        return node_matcher.match(AuthorRepo.label, name=name).first()

    @staticmethod
    def get_author_by_id(graph: Graph, index: int):
        node_matcher = NodeMatcher(graph)
        return node_matcher.match(AuthorRepo.label, index=index).first()

    @staticmethod
    def get_all_author_dict(graph: Graph) -> dict:
        cql = "match (n:Author) return (n);"
        nodes = [x["n"] for x in graph.run(cql).data()]
        return {x["name"]: x for x in nodes}

    @staticmethod
    def get_all_author_name(graph: Graph) -> set:
        cql = "match (n:Author) return (n.name);"
        return set(x["(n.name)"] for x in graph.run(cql).data())

    @staticmethod
    def get_affiliation_list(graph: Graph, author: Author):
        res = []
        for affiliation in author.affiliations:
            node = AffiliationRepo.get_affiliation_by_name(graph, affiliation.name)
            if node is not None:
                res.append(node)
        return res

    @staticmethod
    def get_interest_list(graph: Graph, author: Author):
        res = []
        for interest in author.interests:
            node = InterestRepo.get_interest_by_name(graph, interest.name)
            if node is not None:
                res.append(node)
        return res

    @staticmethod
    def to_neo4j_node(author: Author):
        return Node(AuthorRepo.label, **author.to_dict())
