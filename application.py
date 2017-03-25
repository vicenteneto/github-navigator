import logging
from datetime import datetime
from logging import NullHandler

import requests
from flask import Flask, json, render_template, request
from werkzeug.exceptions import BadRequest

__title__ = 'GitHub Navigator'
__author__ = 'Vicente Neto'

null_handler = NullHandler(logging.INFO)
null_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

BASE_URL = 'https://api.github.com'

app = Flask(__name__, template_folder='')
app.logger.addHandler(null_handler)


def _parse_and_check_github(content):
    """
    Try and parse the JSON returned from GitHub API and raise an exception if there is any error.
    This is a purely defensive check because during some GitHub API network outages or rate limits
    it can return an error.
    """

    try:
        data = json.loads(content.decode('utf-8'))
        if 'message' in data:
            raise Exception(data['message'])
        return data
    except ValueError:
        raise Exception('Unknown error: {0}'.format(content))


def _load_repository_commits(repository):
    """
    Loads all commits from a specific repository and creates a new field with the last committed commit.
    :param repository: The repository object that should have the commits formatted.
    :return: The formatted object.
    """

    url = '{}/repos/{}/commits'.format(BASE_URL, repository['full_name'])

    app.logger.info('Loading commits for repository "%s"', repository['name'])
    response = requests.get(url)

    try:
        commits = _parse_and_check_github(response.content)
        app.logger.info('Last commit found for repository "%s"', repository['name'])
        repository['last_commit'] = commits[0]
    except Exception:
        app.logger.warning('No commits found for repository "%s"', repository['name'])
        pass

    repository['created_at'] = datetime.strptime(repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    return repository


def _search_newest_repositories(search_term):
    """
    Gets the last five repositories created based on a search term.
    :param search_term: The search_term used to search for repositories.
    :return: The five repositories corresponding to the search.
    """

    url = '{}/search/repositories'.format(BASE_URL)

    app.logger.info('Searching repositories with search term equals to "%s"', search_term)
    response = requests.get(url, params={'q': search_term})

    data = _parse_and_check_github(response.content)
    repositories = data['items']
    app.logger.info('Sorting commits by creation date')
    repositories.sort(key=lambda repo: datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
    app.logger.info('Searching for the commits of the first 5 repositories')
    return map(_load_repository_commits, repositories[:5])


@app.route('/navigator')
def list_repositories():
    search_term = request.args.get('search_term', None)
    try:
        if not search_term:
            app.logger.warning('Search term not found in request')
            raise Exception('Search term is required')

        repositories = _search_newest_repositories(search_term)
        app.logger.info('Rendering template with the data obtained')
        return render_template('template.html', search_term=search_term, repositories=repositories)
    except Exception as error:
        app.logger.error('Error: %s', error)
        raise BadRequest(error)


if __name__ == '__main__':
    app.run(port=9876, debug=True)
