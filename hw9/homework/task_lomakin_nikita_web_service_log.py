"""CLI ti parse and print logfile"""
import logging.config
import yaml

from flask import Flask, request, abort, jsonify, make_response
from flask.logging import create_logger
import requests
from bs4 import BeautifulSoup

logging.config.dictConfig(yaml.safe_load(
    """
version: 1.0
formatters:
    simple:
        format: "%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s"
        datefmt: "%Y%m%d_%H%M%S"
handlers:
    stream_handler:
        class: logging.StreamHandler
        stream: ext://sys.stderr
        level: DEBUG
        formatter: simple
loggers:
    task_lomakin_nikita_web_service_log:
        level: DEBUG
        propagate: False
        handlers:
            - stream_handler
root:
    level: DEBUG
    handlers:
        - stream_handler
"""
))

app = Flask(__name__)
app.logger = create_logger(app)

WIKI_BASE_URL = "https://en.wikipedia.org"
WIKI_BASE_SEARCH_URL = f"{WIKI_BASE_URL}/w/index.php?search="


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
    return make_response("Wikipedia Search Engine is unavailable", 503)


@app.route("/api/search")
def api_wiki_proxy_search():
    """roure to search article"""
    user_query = request.args.get("query", "")
    app.logger.debug("start processing query: %s",
                     user_query)  # тут добавил логгер
    wiki_response = requests.get(WIKI_BASE_SEARCH_URL + user_query)
    if not wiki_response.ok:
        abort(503)
    documents_count = parse_article_count(wiki_response.text)
    app.logger.info("found %s articles for query: %s",
                    documents_count, user_query)  # тут  логгер info
    app.logger.debug("finish processing query: %s",
                     user_query)  # тут добавил логгер
    return jsonify({
        "version": 1.0,
        "article_count": documents_count,
    })



def parse_article_count(wiki_search_output):
    """parse artickle count"""
    soup = BeautifulSoup(wiki_search_output, 'html.parser')
    result = soup.find("div", attrs={"class": "results-info"})
    if result is None:
        return 0
    ansver = int(result.findAll("strong")[-1].text.replace(",", ""))
    return ansver
