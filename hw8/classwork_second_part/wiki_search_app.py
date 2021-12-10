from flask import Flask

app = Flask(__name__)

WIKI_BASE_URL = "https://en.wikipedia.org"
WIKI_BASE_SEARCH_URL = f"{WIKI_BASE_URL}/w/index.php?search="
