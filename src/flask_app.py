# This file shows how to add a log handler to flask.
import logging
from logsetup import get_handler
from flask import Flask

app = Flask(__name__)
handler = get_handler({"extra_string": "flask is the task"})
# app.logger.addHandler()
root = logging.getLogger()
root.addHandler(handler)


@app.route("/")
def hello():
    return "Hello World!\n"


@app.route("/foo")
def world():
    return "This is it.\n"
