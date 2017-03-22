import json

import requests

from github_navigator_api.exceptions import GithubError
from github_navigator_api.models import Commit, Repository
from github_navigator_util.constants import Encoding, GithubApi, Response


def _parse_and_check_github(content):
    """
    Try and parse the JSON returned from Github API and raise an exception if there is any error.
    This is a purely defensive check because during some Github API network outages or rate limits
    it can return an error.
    """
    try:

        data = json.loads(content.decode(Encoding.UTF_8))
        if Response.MESSAGE in data:
            raise GithubError(data[Response.MESSAGE])
        return data
    except ValueError:
        raise GithubError('Unknown error: {0}'.format(content))


def _load_repository_commits(repository):
    """
    Loads all commits from a specific repository and creates a new field with the last committed commit.
    :param repository: The repository object that should have the commits formatted.
    :return: The formatted object.
    """

    url = GithubApi.REPOSITORY_COMMITS % repository.full_name

    response = requests.get(url)

    data = _parse_and_check_github(response.content)
    repository.last_commit = Commit.from_dict(data[0]) if data else None
    return repository


def search_newest_repositories(search_term):
    """
    Gets the last five repositories created based on a search term.
    :param search_term: The search_term used to search for repositories.
    :return: The five repositories corresponding to the search.
    """

    url = GithubApi.SEARCH_REPOSITORIES % search_term

    response = requests.get(url)

    data = _parse_and_check_github(response.content)
    repositories = [Repository.from_dict(repository) for repository in data[Response.ITEMS]]
    repositories.sort(key=lambda repo: repo.created_at, reverse=True)
    return map(_load_repository_commits, repositories[:5])
