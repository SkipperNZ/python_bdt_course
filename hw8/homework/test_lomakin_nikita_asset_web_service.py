from flask import request

import pytest
from unittest.mock import patch
from task_lomakin_nikita_asset_web_service import *


HTML_DAILY_DATA_SAMPLE = "cbr_currency_base_daily.html"
HTML_INDICATOR_DATA_SAMPLE = "cbr_key_indicators.html"
HTML_INDICATOR_FROM_WEB = "indicators_from_web.html"
EXPECTED_LEN_OF_DICT_INDICATOR_PARSE = 6


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_parse_cbr_currency_base_daily(capsys):
    expected_result = {
        "AUD": 57.0229,
        "AZN": 44.4127,
        "AMD": 0.144485
    }
    with open(HTML_DAILY_DATA_SAMPLE, "r", encoding="utf8") as fin:
        ansver = parse_cbr_currency_base_daily(fin.read())

    assert 34 == len(ansver), "wrong len of dict"
    assert expected_result["AUD"] == ansver["AUD"], "wrong data"


def test_parse_cbr_key_indicators(capsys):
    expected_result = {
        "USD": 75.4571,
        "EUR": 91.9822,
        "Au": 4529.59,
        "Ag": 62.52,
        "Pt": 2459.96,
        "Pd": 5667.14
    }
    with open(HTML_INDICATOR_DATA_SAMPLE, "r", encoding="utf8") as fin:
        ansver = parse_cbr_key_indicators(fin.read())

    assert expected_result == ansver, "wrong parse indicators"


def test_parse_cbr_key_indicators_from_web(capsys):
    with open(HTML_INDICATOR_FROM_WEB, "r", encoding="utf8") as fin:
        ansver = parse_cbr_key_indicators(fin.read())

    assert EXPECTED_LEN_OF_DICT_INDICATOR_PARSE == len(ansver), "Wrong count of currency and precious metal"


def test_page_not_fount(client):
    expected = "This route is not found"
    app_response = client.get("/not_existed_route")
    assert 404 == app_response.status_code, "status code is not 404"
    assert expected == app_response.data.decode(app_response.charset), "wrong 404 response message"


@patch("requests.get")
def test_cbr_unavailable(mock_get, client):
    expected = "CBR service is unavailable"
    mock_get.return_value.status_code = 503
    app_response = client.get("/cbr/daily")
    assert 503 == app_response.status_code
    assert expected == app_response.data.decode(app_response.charset), "wrong 503 response message"


@patch("requests.get")
def test_cbr_daily_flask_interface(mock_get, client):
    with open(HTML_DAILY_DATA_SAMPLE, "r", encoding="utf8") as fin:
        expected = parse_cbr_currency_base_daily(fin.read())

    with open(HTML_DAILY_DATA_SAMPLE, "r", encoding="utf8") as fin:
        mock_get.return_value.text = fin.read()

    mock_get.return_value.status_code = 200
    app_response = client.get("/cbr/daily")
    expected_json = jsonify(expected).data.decode("utf-8")

    assert expected_json == app_response.data.decode(app_response.charset), "flask app work incorrect" 


@patch("requests.get")
def test_cbr_key_indicator_flask_interface(mock_get, client):
    with open(HTML_INDICATOR_DATA_SAMPLE, "r", encoding="utf8") as fin:
        expected = parse_cbr_key_indicators(fin.read())

    with open(HTML_INDICATOR_DATA_SAMPLE, "r", encoding="utf8") as fin:
        mock_get.return_value.text = fin.read()

    mock_get.return_value.status_code = 200
    app_response = client.get("/cbr/key_indicators")
    expected_json = jsonify(expected).data.decode("utf-8")
    assert expected_json == app_response.data.decode(app_response.charset), "flask app work incorrect"

    
def test_asset():
    asset = Asset("USD", "AAA", 1337, 32.2)

    assert "AAA" == asset.get_name(), "incorrect returned name"
    assert 86102.8 == asset.calculate_revenue(1, 2), "incorrect calculate"


def test_bank():
    asset1 = Asset("USD", "AAA", 1337, 32.2)
    asset2 = Asset("EU", "BBB", 3245, 3.22)
    asset3 = Asset("RUB", "CCC", 1234, 22.8)
    asset4 = Asset("ETH", "DDD", 1234, 22.8)
    bank = Bank()
    bank.add(asset2)
    bank.add(asset1)
    bank.add(asset3)

    assert bank.is_exist(asset1) == True, "is exist doesnt work"
    assert bank.is_exist(asset4) == False, "not existed element return true"


def test_asset_list(client):
    asset1 = Asset("AUSD", "AAA", 1337, 32.2)
    asset2 = Asset("BEU", "BBB", 3245, 3.22)
    asset3 = Asset("CRUB", "CCC", 1234, 22.8)

    client.application.bank = Bank()
    client.application.bank.add(asset2)
    client.application.bank.add(asset3)
    client.application.bank.add(asset1)

    expected_result = [['AUSD', 'AAA', 1337, 32.2],
                         ['BEU', 'BBB', 3245, 3.22],
                         ['CRUB', 'CCC', 1234, 22.8]]

    app_response = client.get("/api/asset/list")

    assert 200 == app_response.status_code, "qwerty"
    assert expected_result == app_response.json, "qwerty"


   
def test_get_flask(client, capsys):
    asset1 = Asset("AUSD", "Jojo", 1337, 32.2)
    asset2 = Asset("BEU", "BBB", 3245, 3.22)
    asset3 = Asset("CRUB", "CCC", 1234, 22.8)

    client.application.bank = Bank()
    client.application.bank.add(asset2)
    client.application.bank.add(asset3)
    client.application.bank.add(asset1)

    expected_result = '[["AUSD","Jojo",1337,32.2]]\n'

    route = "/api/asset/get?name=Jojo&name=Referense"
    response = client.get(route)

    assert expected_result == response.data.decode(response.charset)
