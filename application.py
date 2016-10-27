__author__ = 'mateusz'

import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "OK"


if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 8080))