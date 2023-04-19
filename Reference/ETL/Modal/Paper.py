# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 21点16分
@Function: 请描述这个py文件的作用
"""
from Modal.Author import Author


class Paper:
    def __init__(self, index=-1, title="", year=-1, authors=None, venue="", cites=None, abstract=""):
        if authors is None:
            authors = []
        if cites is None:
            cites = []

        self.index = index
        self.title = title
        self.year = year
        self.authors = authors
        self.venue = venue
        self.cites = cites
        self.abstract = ""
        self.set_abstract(abstract)

    def to_dict(self):
        return {
            "index": self.index,
            "title": self.title,
            "year": self.year,
            "abstract": self.abstract
        }

    def get_write_relations(self):
        res = []
        length = len(self.authors)
        if length > 0:
            res.append(WriteRelation(author=self.authors[0], paper=self))
        return res

    def get_participate_relations(self):
        res = []
        length = len(self.authors)
        for i in range(1, length):
            res.append(ParticipateRelation(author=self.authors[i], paper=self))
        return res

    def get_cite_relations(self):

        return [CiteRelation(paper=self, cite=cite) for cite in self.cites]

    def get_publication_relations(self):
        if self.venue:
            return [PublicationRelation(paper=self, venue=self.venue)]
        else:
            return []

    def set_index(self, index):
        self.index = index

    def set_title(self, title):
        self.title = title

    def set_year(self, year):
        self.year = year

    def set_authors(self, authors):
        self.authors = [Author(name=author) for author in authors]

    def set_venue(self, venue):
        self.venue = venue

    def set_cites(self, cite):
        self.cites.append(cite)

    def set_abstract(self, abstract):
        self.abstract = \
            abstract.replace("\\", "") \
                .replace("\"", "") \
                .replace("\'", "")


class WriteRelation:
    def __init__(self, author: Author, paper: Paper):
        self.author = author
        self.paper = paper

    def to_dict(self):
        return {
            "author": self.author.name,
            "paper": self.paper.index
        }


class ParticipateRelation:
    def __init__(self, author: Author, paper: Paper):
        self.paper = paper
        self.author = author

    def to_dict(self):
        return {
            "paper": self.paper.index,
            "author": self.author.name
        }


class CiteRelation:
    def __init__(self, paper: Paper, cite: int):
        self.paper = paper
        self.cite = cite

    def to_dict(self):
        return {
            "paper": self.paper.index,
            "cite": self.cite
        }


class PublicationRelation:
    def __init__(self, paper: Paper, venue: str):
        self.paper = paper
        self.venue = venue

    def to_dict(self):
        return {
            "paper": self.paper.index,
            "venue": self.venue
        }
