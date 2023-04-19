# coding:utf-8
"""
@file: .py
@author: dannyXSC
@ide: PyCharm
@createTime: 2022年05月04日 20点49分
@Function: 工具函数
"""
import time

import yaml
from EnvironmentVariable import *


def get_neo4j_info():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["neo4j"]
            return obj["url"], obj["account"], obj["password"]
        except yaml.YAMLError as exc:
            print(exc)
            return "" "" ""


def get_author_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["AMiner"]
            return obj["author_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_coauthor_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["AMiner"]
            return obj["coauthor_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["AMiner"]
            return obj["paper_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_author_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["author_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_author_affiliation_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["author_affiliation_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_author_interest_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["author_interest_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["paper_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_write_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["paper_write_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_cite_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["paper_cite_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_publication_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["paper_publication_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_paper_participate_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["paper_participate_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def get_coauthor_csv_path():
    with open(resource_path, "r") as stream:
        try:
            obj = yaml.safe_load(stream)["CSV"]
            return obj["coauthor_path"]
        except yaml.YAMLError as exc:
            print(exc)
            return ""


def timer(keyword=''):
    def func(fun):
        def wrapper(*args, **kwargs):
            print(fun.__name__ + f" {keyword}开始计时")
            time_start = time.time()
            result = fun(*args, **kwargs)
            time_end = time.time()
            cost_time = time_end - time_start
            print(fun.__name__ + f" {keyword}耗时：{cost_time}秒")
            return result

        return wrapper

    return func
