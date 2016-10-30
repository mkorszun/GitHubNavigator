import requests
from flask.json import jsonify
from datetime import datetime

import os
from flask import Flask

from webargs import fields
from webargs.flaskparser import use_args
from flask import render_template

REPO_SEARCH_QUERY = 'https://api.github.com/search/repositories?q={0}'
COMMITS_SEARCH_QUERY = 'https://api.github.com/repos/{0}/{1}/commits'

app = Flask(__name__)


@app.route("/")
def index():
    return "OK"


@app.route("/navigator")
@use_args({'search_term': fields.Str(required=True, location='query')})
def search(args):
    search_term = args['search_term']
    response = requests.get(REPO_SEARCH_QUERY.format(search_term))

    if response.status_code != 200:
        app.logger.error('Failed to fetch repositories from Github: %s', response.text)
        return 'Failed to fetch repositories from Github', 500

    repositories = sorted(response.json()['items'], key=lambda repo: str_to_datetime(repo['created_at']), reverse=True)[:5]
    repositories_with_commits = [set_last_commit(repository) for repository in repositories]
    return render_template('template.html', items=repositories_with_commits, search_term=search_term)


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


def str_to_datetime(created_at):
    return datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')


def set_last_commit(repo):
    response = requests.get(COMMITS_SEARCH_QUERY.format(repo['owner']['login'], repo['name']))

    if response.status_code != 200:
        app.logger.error('Failed to fetch commits for repo=%s: %s', repo['name'], response.text)
        return repo

    last_commit = response.json()[0]
    repo['last_commit_sha'] = last_commit['sha'] if last_commit else None
    repo['last_commit_msg'] = last_commit['commit']['message'] if last_commit else None
    repo['last_commit_author'] = last_commit['commit']['author']['name'] if last_commit else None
    return repo


if __name__ == "__main__":
    app.run(port=os.getenv('PORT', 8080))
