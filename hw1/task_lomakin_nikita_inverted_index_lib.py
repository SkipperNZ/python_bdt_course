"""Inverted index 1st task"""
from __future__ import annotations
from typing import Dict, List
from collections import defaultdict
import re
import json


class InvertedIndex:
    """this is class Inverted index """

    def __init__(self, idx: dict[str, list[int]]):
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


def main():
    """pylint is grumbles that this have no describe"""
    documents = load_documents("./mini_wiki.txt")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("invertedindex.json")
    inverted_index = InvertedIndex.load("invertedindex.json")
    document_ids = inverted_index.query(["two", "words"])


if __name__ == "__main__":
    main()
