from flask import Flask, redirect, url_for, abort
from markupsafe import escape

app = Flask(__name__)

DEFAULT_GREATING_COUNT = 10
MAX_GREATING_COUNT = 100
REALY_TOO_MANEY_GREATING_COUNT = 1000

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/hello/<string:username>/")
# декораторы можно дублировать num изначально в формате str
@app.route("/hello/<string:username>/<int:num>")
def personal_greetings(username, num=DEFAULT_GREATING_COUNT):
    if num >= REALY_TOO_MANEY_GREATING_COUNT:
        abort(404)
    if num > MAX_GREATING_COUNT:
        return redirect(url_for("personal_greetings", username=username, num=DEFAULT_GREATING_COUNT))

    greatings = ["Hello, " + escape(username) + "!"] * num
    return "<br/>".join(greatings)
