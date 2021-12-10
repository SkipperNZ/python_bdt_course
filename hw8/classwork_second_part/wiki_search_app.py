from flask import Flask, request
import requests

app = Flask(__name__)

WIKI_BASE_URL = "https://en.wikipedia.org"
WIKI_BASE_SEARCH_URL = f"{WIKI_BASE_URL}/w/index.php?search="


@app.route("/search")
def wiki_proxy_search():
    user_query = request.args.get("query", "")
    wiki_response = requests.get(WIKI_BASE_SEARCH_URL + user_query )
    return wiki_response.text, wiki_response.status_code   