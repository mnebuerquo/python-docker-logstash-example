# This file shows how to add a log handler to flask.
import logging
from logsetup import get_handler
from request_formatter import RequestFormatter
from flask import Flask

app = Flask(__name__)
formatter = RequestFormatter({"extra_string": "flask is the task"})
handler = get_handler(formatter=formatter)
root = logging.getLogger()
root.addHandler(handler)


@app.route("/")
def hello():
    return "Hello World!\n"


@app.route("/foo")
def world():
    return "This is it.\n"
