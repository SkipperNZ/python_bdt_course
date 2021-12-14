#!/usr/bin/env python3
"""
Asset web service
"""

from flask import Flask, request, abort, jsonify, make_response, Response
import requests
from bs4 import BeautifulSoup
from typing import Dict, List


CBR_BASE_URL = "https://www.cbr.ru/eng"
CBR_DAILY_URL = f"{CBR_BASE_URL}/currency_base/daily/"
CBR_KEY_INDICATORS_URL = f"{CBR_BASE_URL}/key-indicators/"


class Asset:
    def __init__(self, char_code: str, name: str, capital: float, interest: float):
        self.char_code = char_code
        self.name = name
        self.capital = capital
        self.interest = interest

    def get_name(self) -> str:
        return self.name

    def get_list_asset(self) -> List:
        return [self.char_code, self.name, self.capital, self.interest]

    def calculate_revenue(self, years: int, rate: float) -> float:
        """calculate_revenue"""
        revenue = rate * self.capital * ((1.0 + self.interest) ** years - 1.0)
        return revenue


class Bank:
    """
    Asset storage
    """

    def __init__(self):
        """ asset_collection"""
        self.asset_collection = {}

    def add(self, item: Asset):
        """add new asset in bank"""
        self.asset_collection[item.get_name()] = item

    def is_exist(self, item: Asset) -> bool:
        """check does asset in bank"""
        if self.asset_collection.get(item.get_name()) == None:
            return False
        else:
            return True

    def get_list(self):
        """
        get sorted list of asset
        """
        result = []
        for item in self.asset_collection.values():
            result.append(item.get_list_asset())
        result.sort()
        return result

    def get_asset(self, name: str):
        ansver = self.asset_collection.get(name)
        if ansver == None:
            return None
        else:
            return ansver.get_list_asset()

    def calculate_total_revenue(self,
                                period: int, 
                                indicators_dict: Dict[str, float],
                                daily_dict: Dict[str, float],) -> float:
        """
        calculate total revenue
        """
        ansver = 0.0
        for item in self.asset_collection.values():
            if  item.char_code in indicators_dict:
                rate_of_item = indicators_dict[item.char_code]
            else:
                rate_of_item = daily_dict.get(item.char_code, 0)
            ansver += item.calculate_revenue(period, rate_of_item)
        return ansver

    def clear(self):
        """clear all assets"""
        self.asset_collection.clear()





app = Flask(__name__)
app.bank = Bank()


def parse_cbr_currency_base_daily(html_data: str) -> Dict[str, float]:
    """
    parse_cbr_currency_base_daily
    Parse https://www.cbr.ru/eng/currency_base/daily/
    {“char_code”: rate}
    char_code - буквенный код
    rate - курс валют в обмене на 1 у.е.
    """
    parsing_result = {}
    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find("table", attrs={"class": "data"})
    tbody = table.find('tbody')
    row_collection = tbody.find_all('tr')

    for row in row_collection:
        cells = row.find_all('td')
        if len(cells) != 5:
            continue
        char_code = cells[1].text
        unit = float(cells[2].text)
        rate_from_table = float(cells[4].text)
        true_rate = rate_from_table / unit
        parsing_result[char_code] = true_rate
    return parsing_result


def parse_cbr_key_indicators(html_data: str) -> Dict[str, float]:
    """
    parse https://www.cbr.ru/eng/key-indicators/
    {“char_code”: rate}
    char_code - буквенный код
    rate - стоимость 
    """
    parsing_result = {}

    soup = BeautifulSoup(html_data, 'html.parser')
    dropdown_table_collection = soup.findAll(
        "div", attrs={"class": "dropdown"})

    for table in dropdown_table_collection:
        if table.findAll("div", attrs={"class": "dropdown_title _active"}) != []:
            table_with_currency_and_metal = table
    subtable_collection = table_with_currency_and_metal.findAll("div",
                                                                attrs={"class": "key-indicator_content offset-md-2"})
    for subtable in subtable_collection:
        if subtable.findAll("div",
                            attrs={"class": "d-flex flex-column flex-md-row title-date"}) != []:
            continue
        rows = subtable.find_all("tr")
        for row in rows[1:]:
            char_code = row.find("div",
                                 attrs={"class": "col-md-3 offset-md-1 _subinfo"}).text
            rate = float(row.findAll("td")[-1].text.replace(",", ""))
            parsing_result[char_code] = rate

    return parsing_result


@app.errorhandler(404)
def page_not_found(error):
    """
    404 error
    """
    return "This route is not found", 404


@app.errorhandler(500)
def cbr_unavailable(error):
    """
    503 error
    """
    return make_response("CBR service is unavailable", 503)


@app.route("/cbr/daily")
def get_cbr_daily():
    """
    parse data from
    "https://www.cbr.ru/eng/currency_base/daily/"
    return: Json with parsed data
    """
    response = requests.get(CBR_DAILY_URL)
    result = parse_cbr_currency_base_daily(response.text)
    return jsonify(result)


@app.route("/cbr/key_indicators")
def get_cbr_key_indicators():
    """
    parse data from
    https://www.cbr.ru/eng/key-indicators/
    :return: Json with parsed data
    """
    response = requests.get(CBR_KEY_INDICATORS_URL)
    result = parse_cbr_key_indicators(response.text)
    return jsonify(result)


@app.route("/api/asset/add/<string:char_code>/<string:name>/<string:capital>/<string:interest>")
def add_asset_flask(char_code: str, name: str, capital: str, interest: str):
    """
    добавить актив в валюте “char_code” с именем “name”, размером капитала
    capital и оценочной инвестиционной годовой доходностью interest (в процентах,
    записанных дробным числом; то есть в качестве interest можно указать число 0.5, что
    будет означать 50%). Запрос должен возвращать код возврата 200 и сообщение "Asset
    '{name}' was successfully added". В случае попытки добавления актива с именем (name),
    который уже существует в базе, система должна выдавать код возврата 403.
    """
    income_asset = Asset(
        char_code=char_code,
        name=name,
        capital=float(capital),
        interest=float(interest),
    )

    if app.bank.is_exist(income_asset):
        return make_response(f"Asset '{name}' has already exist", 403)
    app.bank.add(income_asset)
    return make_response(f"Asset '{name}' was successfully added", 200)


@app.route("/api/asset/list")
def asset_list_flask():
    """
    return json(list) of all asset
    """
    answer = app.bank.get_list()
    return jsonify(answer)


@app.route("/api/asset/get")
def asset_get_flask():
    """
    return json(list) of selected asset
    """
    answer = []
    name_collection = request.args.getlist("name")

    for name in name_collection:
        asset = app.bank.get_asset(name)
        if asset != None:
            answer.append(asset)

    answer.sort()
    return jsonify(answer)


@app.route("/api/asset/calculate_revenue")
def asset_calculate_revenue_flask():
    """
    calculate revenue to periods
    return {“period”: revenue},
    """
    answer = dict()

    periods = request.args.getlist('period')
    cbr_key_indicators_response = requests.get(CBR_KEY_INDICATORS_URL)
    cbr_daily_response = requests.get(CBR_DAILY_URL)

    # {“char_code”: rate}
    indicators_dict = parse_cbr_key_indicators(
        cbr_key_indicators_response.text)
    daily_dict = parse_cbr_currency_base_daily(cbr_daily_response.text)

    for period in periods:
        answer[int(period)] = app.bank.calculate_total_revenue(
            period=int(period),
            indicators_dict=indicators_dict,
            daily_dict=daily_dict)

    return jsonify(answer)


@app.route("/api/asset/cleanup")
def clear_api():
    """
    clear all asser from bank
    return: message and response 200
    """
    app.bank.clear()
    return make_response("there are no more assets", 200)
