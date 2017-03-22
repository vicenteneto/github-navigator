class Config(object):
    CONFIG = 'Config'
    DEVELOPMENT_CONFIG = 'Development' + CONFIG
    PRODUCTION_CONFIG = 'Production' + CONFIG
    TESTING_CONFIG = 'Testing' + CONFIG


class Encoding(object):
    UTF_8 = 'utf-8'


class GithubApi(object):
    BASE_URL = 'https://api.github.com'
    REPOSITORY_COMMITS = BASE_URL + '/repos/%s/commits'
    SEARCH_REPOSITORIES = BASE_URL + '/search/repositories?q=%s'


class Response(object):
    ITEMS = 'items'
    MESSAGE = 'message'
