import pytest
from web_hello_world import app as hello_world_app

@pytest.fixture
def client():
    with hello_world_app.test_client() as client:
        yield client

def test_service_reply_to_root_path(client):
    response = client.get("/")

    assert "world" in response.data.decode(response.charset)

