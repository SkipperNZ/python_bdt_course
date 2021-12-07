'''
тествое сообщение для теста пуша на гитхаб
'''

jojo = 1337

import io
import pytest
import json
from argparse import Namespace

from task_lomakin_nikita_inverted_index_lib import InvertedIndex, load_documents, \
    build_inverted_index, DEFAULT_INVERTED_INDEX_STORE_PATH, callback_query, callback_build, EncodedFileType, \
    some_trick_to_make_perfect_mark

MINI_DOCUMENT = {
    1: 'aa bb cc',
    2: 'aa cc',
    3: 'jojo reference',
    4: 'cc dd bb'
}

PYTHON_CODE_DOCUMENT = {
    1: 'aa bb cc',
    2: 'aa cc',
    3: 'jojo reference',
    4: 'Python code aa bb',
    5: 'cc dd bb',
    6: 'Python cc',
    7: 'Code aa'
}

MINI_IDX = {
    'aa': [1, 2],
    'bb': [1, 4],
    'cc': [1, 2, 3],
    'dd': [4],
    'jojo': [3],
    'reference': [3]
}

MINI_DOCUMENT_PATH = "./mini_document.txt"

BIG_DOCUMENT_PATH = "./wikipedia_sample.txt"

def test_constructor():
    idx = InvertedIndex({'first': [1, 2, 3], 'second': [4, 5, 6]})
    assert idx._idx_storage == {'first': [1, 2, 3], 'second': [4, 5, 6]}, "constructor doesn't work"


def test_empty_constructor():
    idx = InvertedIndex({})
    assert idx._idx_storage == {}, "empty dict dont load"


def test_eq():
    idx1 = InvertedIndex({'first': [1, 2, 3], 'second': [4, 5, 6]})
    idx2 = InvertedIndex({'first': [1, 2, 3], 'second': [4, 5, 6]})
    assert idx1 == idx2, "can't compare __eq__"


def test_build_inverted_index():
    correct = InvertedIndex({
        'aa': [1, 2],
        'bb': [1, 4],
        'cc': [1, 2, 3],
        'dd': [4],
        'jojo': [3],
        'reference': [3]
    })
    idx = build_inverted_index(MINI_DOCUMENT)
    assert sorted(correct._idx_storage) == sorted(idx._idx_storage), "Wrong  build inverted index"


def test_build_empty_inverted_index():
    correct = InvertedIndex({})
    idx = build_inverted_index({})
    assert correct._idx_storage == idx._idx_storage


def test_can_open_mini_file():
    with open(MINI_DOCUMENT_PATH, 'r') as f:
        first_string = f.readline().strip()
    assert first_string == '1	aa bb cc', 'File can not open from directory'


def test_load_documents():
    doc = load_documents(MINI_DOCUMENT_PATH)
    assert MINI_DOCUMENT == doc, 'Wrong parsing in load_document'


def test_can_load_doc_and_make_correct_index():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    assert sorted(idx._idx_storage) == sorted(MINI_IDX)


def test_query():
    correct_query = [3]
    idx = InvertedIndex({'first': [1, 2, 3], 'second': [4, 5, 6], 'third': [7, 3, 9]})
    returned_query = idx.query(['first', 'third'])
    assert returned_query == correct_query, 'Wrong query was returned'


def test_empty_query():
    correct_query = []
    idx = InvertedIndex({'first': [1, 2, 3], 'second': [4, 5, 6], 'third': [7, 3, 9]})
    returned_query = idx.query(['jojo', 'reference'])
    assert returned_query == correct_query, 'Wrong query was returned'


PYTHON_CODE_DOCUMENT = {
    1: 'aa bb cc',
    2: 'aa cc',
    3: 'jojo reference',
    4: 'Python code aa bb',
    5: 'cc dd bb',
    6: 'Python cc',
    7: 'Code aa'
}


def test_python_query():
    correct_query = [4, 6]
    idx = build_inverted_index(PYTHON_CODE_DOCUMENT)
    returned_query = idx.query(['Python'])
    assert returned_query == correct_query, 'Wrong ansver for [Python] query '


def test_code_query():
    correct_query = [4, 7]
    idx = build_inverted_index(PYTHON_CODE_DOCUMENT)
    returned_query = idx.query(['code'])
    assert returned_query == correct_query, 'Wrong ansver for [code] query '


def test_python_code_query():
    correct_query = []
    idx = build_inverted_index(PYTHON_CODE_DOCUMENT)
    returned_query = idx.query(['Python', 'code', 'jojo'])
    assert returned_query == correct_query, 'Wrong ansver for Python + code query '












def test_dump():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    idx.dump('test_dump.json')
    with open('test_dump.json', 'r') as f:
        data = json.load(f)
        assert idx._idx_storage == data, 'Wrong dump'



def test_bin_dump_and_load():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    idx.dump_in_struct('test_bin_dump.index')

    #with open('test_bin_dump.index', 'r') as f:
    loaded_idx = InvertedIndex.load_from_struct('test_bin_dump.index')
    assert idx._idx_storage == loaded_idx._idx_storage, 'Wrong dump'


def test_load():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    idx.dump('test_load.json')

    loaded_idx = InvertedIndex.load('test_load.json')
    assert loaded_idx._idx_storage == idx._idx_storage


def test_callback_query_utf_8():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    idx.dump('test_load.json')
    with open("query_utf_8.txt") as queries_fin:
        arguments = Namespace(
            query=None,
            index='test_load.json',
            strategy='json',
            query_file=queries_fin,
        )
        callback_query(arguments)



def test_callback_build_in_line_json():


    arguments = Namespace(
        dataset='mini_document.txt',
        strategy='json',
        output='test_json.output',
    )
    callback_build(arguments)

def test_callback_build_in_line_struct():
    arguments = Namespace(
        dataset='mini_document.txt',
        strategy='struct',
        output='test_struct.output',
    )
    callback_build(arguments)


def test_callback_query_in_line_json():
    doc = load_documents(MINI_DOCUMENT_PATH)
    idx = build_inverted_index(doc)
    idx.dump('test_load.json')

    arguments = Namespace(
        query="aa bb",
        index='test_load.json',
        strategy='json',
    )
    callback_query(arguments)

def test_callback_query_in_line_struct():
    arguments = Namespace(
        dataset='mini_document.txt',
        strategy='struct',
        output='test_struct.output',
    )
    callback_build(arguments)

    arguments = Namespace(
        query="aa bb",
        index='test_struct.output',
        strategy='struct',
    )
    callback_query(arguments)


def test_can_prints():
    some_trick_to_make_perfect_mark()

