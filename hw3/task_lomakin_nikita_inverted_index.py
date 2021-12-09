#!/usr/bin/env python3
"""Inverted index 1st task"""
from __future__ import annotations

import sys
from typing import Dict, List
from collections import defaultdict
import re
import json
import struct
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from io import TextIOWrapper

DEFAULT_DATASET_PATH = "wikipedia_sample.txt"
DEFAULT_INVERTED_INDEX_STORE_PATH = "inverted.index"


class EncodedFileType(FileType):
    """fix"""
    def __call__(self, input_string):
        if input_string == '-':
            if 'r' in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
                return stdin
            if 'w' in self._mode:
                stdout = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
                return stdout
            msg = 'argument "-" with mode %r' % self._mode
            raise ValueError(msg)
        try:
            return open(input_string, self._mode, self._bufsize, self._encoding, self._errors)
        except OSError as os_error:
            message = "can't open '%s': %s"
            raise ArgumentTypeError(message % (input_string, os_error)) from os_error


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

    def dump_in_struct(self, filepath: str) -> None:
        """dump inverted index in struct format"""
        print(f"saving inverted index into {filepath}", file=sys.stderr)

        with open(filepath, 'wb') as fio:
            for word in self._idx_storage:
                encoded_word = word.encode()
                fio.write(struct.pack(">H", len(encoded_word)))
                fio.write(encoded_word)
                ids_for_word = self._idx_storage[word]
                fio.write(struct.pack('>H', len(ids_for_word)))
                fio.write(struct.pack(f'>{len(ids_for_word)}H', *ids_for_word))

            fio.close()

    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        """load inverted index from main derectory"""
        with open(filepath, "r", encoding='utf-8') as file_to_read:
            data = json.load(file_to_read)

        return InvertedIndex(data)

    @classmethod
    def load_from_struct(cls, filepath: str) -> InvertedIndex:
        """load inverted index from binary file in main derectory"""

        with open(filepath, 'rb') as fio:
            file_size = os.path.getsize(filepath)

            loaded_index = {}

            while fio.tell() < file_size:
                lenth_of_segment = struct.calcsize('>H')

                lenth_of_word_int = struct.unpack('>H', fio.read(lenth_of_segment))[0]
                lenth_of_word_bite = struct.calcsize(
                    f'>{lenth_of_word_int}s')
                word = struct.unpack(f'>{lenth_of_word_int}s',
                                     fio.read(lenth_of_word_bite))[0].decode()

                lenth_of_list_int = struct.unpack('>H', fio.read(lenth_of_segment))[0]
                lenth_of_list_bite = struct.calcsize(f'>{lenth_of_list_int}H')
                list_of_idxs = list(struct.unpack(f'>{lenth_of_list_int}H',
                                                  fio.read(lenth_of_list_bite)))
                loaded_index[word] = list_of_idxs

        return InvertedIndex(loaded_index)

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
    documents = load_documents(arguments.dataset)
    inverted_index = build_inverted_index(documents)

    if arguments.strategy == 'json':
        inverted_index.dump(arguments.output)
    elif arguments.strategy == 'struct':
        inverted_index.dump_in_struct(arguments.output)


def callback_query(arguments):
    """callback function for query"""
    print(f"call query subcommand with arguments: {arguments}", file=sys.stderr)
    if arguments.strategy == 'json':
        inverted_index = InvertedIndex.load(arguments.index)
    elif arguments.strategy == 'struct':
        inverted_index = InvertedIndex.load_from_struct(arguments.index)

    if arguments.query is not None:
        for single_query in arguments.query:
            returned_query = inverted_index.query(single_query)
            print(",".join(list(map(str, returned_query))))
    else:
        for single_query in arguments.query_file:
            single_query = single_query.strip().split()
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
        choices=['json', 'struct'],
        default='struct',
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
        "--index",
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="path to read inverted index",
    )

    query_parser.add_argument(
        "-s", "--strategy",
        choices=['json', 'struct'],
        default='struct',
        required=False,
        help="choice index strategy on disk default is %(default)s",
    )

    query_file_group = query_parser.add_mutually_exclusive_group(required=True)

    query_file_group.add_argument(
        "-q", "--query",
        nargs="+",
        help="query to run against inverted index in defoult utf-8",
        action='append',
    )

    query_file_group.add_argument(
        "--query-file-utf8",
        type=EncodedFileType("r", encoding="utf-8"),
        dest="query_file",
        help="query to run against inverted index in implicit utf-8",
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
    )

    query_file_group.add_argument(
        "--query-file-cp1251",
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        dest="query_file",
        type=EncodedFileType("r", encoding="cp1251"),
        help="query to run against inverted index in implicit cp1251",
    )


def main():
    """p_y_l_i_n_t is grumbles that this have no describe"""

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
