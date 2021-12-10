from flask import request

import pytest
from  wiki_search_app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_can_proxy_request_to_wiki(client):
    app_response = client.get("/search?query=python network")
    assert 200 == app_response.status_code
    assert "NetworkX" in app_response.data.decode(app_response.charset)