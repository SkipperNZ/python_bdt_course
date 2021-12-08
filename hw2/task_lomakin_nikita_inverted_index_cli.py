#!/usr/bin/env python3
"""Inverted index 1st task"""
from __future__ import annotations

import sys
from typing import Dict, List
from collections import defaultdict
import re
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

DEFAULT_DATASET_PATH = "wikipedia_sample.txt"
DEFAULT_INVERTED_INDEX_STORE_PATH = "inverted.index"


class InvertedIndex:
    """this is class Inverted index """

    def __init__(self, idx: Dict[str, List[int]]):
        self._idx_storage = idx

    def query(self, words: List[str]) -> List[int]:
        """Return the list of relevant documents for the given query"""
        ans = set()
        words = [x.lower() for x in words]
        flag = True

        for word in words:
            documents_id = set(self._idx_storage.get(word, []))
            if flag:
                ans = documents_id
                flag = False
            else:
                ans.intersection_update(documents_id)
        return list(ans)

    def dump(self, filepath: str) -> None:
        """dump inverted index in main derectory"""
        with open(filepath, "w", encoding='utf8') as file_to_write:
            json.dump(self._idx_storage, file_to_write)

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        """load inverted index from main derectory"""
        with open(filepath, "r", encoding='utf-8') as file_to_read:
            data = json.load(file_to_read)

        return InvertedIndex(data)

    def __eq__(self, rhs_inverted_index):
        ans = (self._idx_storage == rhs_inverted_index._idx_storage)
        return ans


def load_documents(filepath: str) -> Dict[int, str]:
    """load txt documents from main derectory"""
    doc = defaultdict(str)
    with open(filepath, 'r', encoding='utf-8') as fio:
        lines = fio.readlines()
    for line in lines:
        doc_id, content = line.lower().split("\t", 1)
        doc_id = int(doc_id)
        doc[doc_id] = content.strip()

    return doc


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    """Build inverted index from parsed document from load_documents"""
    idx_set = defaultdict(set)
    idx_list = defaultdict(list)
    for doc_id, content in documents.items():
        content = content.lower()
        for word in re.split(r"\W+", content):
            idx_set[word].add(doc_id)

    for key, value in idx_set.items():
        idx_list[key] = list(value)

    return InvertedIndex(dict(idx_list))


def callback_build(arguments):
    """callback function for build"""
    print(f"call build subcommand with arguments: {arguments}", file=sys.stderr)
    if arguments.strategy == 'json':
        documents = load_documents(arguments.dataset)
        inverted_index = build_inverted_index(documents)
        inverted_index.dump(arguments.output)
    elif arguments.strategy == 'pickle':
        raise NotImplementedError("strategy pickle is not done,use json insteed")


def callback_query(arguments):
    """callback function for query"""
    print(f"call query subcommand with arguments: {arguments}", file=sys.stderr)

    inverted_index = InvertedIndex.load(arguments.json_index)

    for single_query in arguments.query:
        returned_query = inverted_index.query(single_query)
        print(",".join(list(map(str, returned_query))))


def setup_parser(parser):
    """Setups parser"""
    subparsers = parser.add_subparsers(help="choose comand")

    build_parser = subparsers.add_parser(
        "build",
        help="build inverted index and save into hard drive",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    build_parser.set_defaults(callback=callback_build)

    build_parser.add_argument(
        "-s", "--strategy",
        choices=['json', 'pickle'],
        default='json',
        required=False,
        help="choice strategy to build index default is %(default)s",
    )

    build_parser.add_argument(
        "-d", "--dataset",
        default=DEFAULT_DATASET_PATH,
        required=False,
        help="path to dataset to load, default path is %(default)s",
    )

    build_parser.add_argument(
        "-o", "--output",
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        required=False,
        help="path to store inverted index in a binary format, default path is %(default)s",
    )

    query_parser = subparsers.add_parser(
        "query",
        help="query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    query_parser.set_defaults(callback=callback_query)

    query_parser.add_argument(
        "--json-index",
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="path to read inverted index",
    )

    query_parser.add_argument(
        "-q", "--query",
        required=True,
        nargs="+",
        help="query to run against inverted index",
        action='append',
    )


def main():
    """pylint is grumbles that this have no describe"""

    parser = ArgumentParser(
        prog="inverted-index",
        description="tool to build, dump load and query inverted index Inverted Index CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
