from flask import request


import pytest
from  task_lomakin_nikita_web_service_log import *


FIRST_PYTHON_NETWORK_RESULT = [
        "Python (programming language)",
        "/wiki/Python_(programming_language)",
        "Python is an interpreted high-level general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant"
]


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_parse_article_count(capsys):
    wiki_response = requests.get(WIKI_BASE_SEARCH_URL + "<bloomberg>" )
    assert 200 == wiki_response.status_code
    result = parse_article_count(wiki_response.text)

    assert result > 40000, "article count dont parse"


def test_can_proxy_request_to_wiki(client):
    app_response = client.get("/api/search?query=python network")
    assert 200 == app_response.status_code


