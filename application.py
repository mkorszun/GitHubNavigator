from flask.json import jsonify

__author__ = 'mateusz'

import os
from flask import Flask

from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)


@app.route("/")
def index():
    return "OK"


@app.route("/navigator")
@use_args({'search_term': fields.Str(required=True, location='query')})
def search(args):
    search_term = args['search_term']
    return "OK"


@app.errorhandler(422)
def args_error_handler(err):
    data = getattr(err, 'data')
    if data:
        messages = data['messages']
    else:
        messages = ['Invalid request']
    return jsonify({
        'error': messages,
    }), 422


if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 8080))