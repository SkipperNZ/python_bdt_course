from flask import Flask, redirect, url_for, abort, render_template
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

@app.errorhandler(404)
def page_do_not_exist(error):
    return render_template("page_not_found.html"), 404  # переименовали index.html в page_not_found.html
