import pytest
from web_hello_world import app as hello_world_app, DEFAULT_GREATING_COUNT, MAX_GREATING_COUNT, REALY_TOO_MANEY_GREATING_COUNT


@pytest.fixture
def client():
    with hello_world_app.test_client() as client:
        yield client


def test_service_reply_to_root_path(client):
    response = client.get("/")
    assert "World" in response.data.decode(response.charset)


def test_service_reply_to_username_with_default_num(client):
    '''персональное приветствие'''
    username = "Vasya"
    response = client.get(f"/hello/{username}", follow_redirects=True)
    response_text = response.data.decode(response.charset)
    vasya_count = response_text.count(username)
    assert DEFAULT_GREATING_COUNT == vasya_count


def test_service_reply_to_username_several_times(client):
    '''персональное приветствие для пети 15 раз'''
    username = "Petya"
    expected_greating_count = 15
    response = client.get(f"/hello/{username}/{expected_greating_count}")
    response_text = response.data.decode(response.charset)
    petya_count = response_text.count(username)
    assert expected_greating_count == petya_count


def test_service_reply_to_escaped_username(client):
    '''проверяем на ескейпирование тегов'''
    non_escaped_tag = "<br>"
    username = "Petya"
    expected_greating_count = 15
    response = client.get(
        f"/hello/{non_escaped_tag}{username}/{expected_greating_count}")
    response_text = response.data.decode(response.charset)
    petya_count = response_text.count(username)
    assert expected_greating_count == petya_count
    assert 0 == response_text.count(non_escaped_tag)


def test_service_hello_to_username_with_slash(client):
    username = "Vasya"
    response = client.get(f"/hello/{username}/")

    assert 200 == response.status_code


def test_service_reply_to_username_with_too_many_num(client):
    '''персональное приветствие для пети 15 раз'''
    username = "Petya"
    suplied_greating_count = MAX_GREATING_COUNT + 1
    expected_greating_count = DEFAULT_GREATING_COUNT
    response = client.get(
        f"/hello/{username}/{suplied_greating_count}", follow_redirects=True)
    response_text = response.data.decode(response.charset)
    petya_count = response_text.count(username)
    assert expected_greating_count == petya_count


def test_service_reply_to_username_with_realy_too_many_num(client):
    '''персональное приветствие для пети 15 раз'''
    username = "Petya"
    suplied_greating_count = REALY_TOO_MANEY_GREATING_COUNT + 1
    response = client.get(
        f"/hello/{username}/{suplied_greating_count}", follow_redirects=True)
    assert 404 == response.status_code
    response_text = response.data.decode(response.charset)
    petya_count = response_text.count(username)
    assert 0 == petya_count
