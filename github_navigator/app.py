from flask import Flask

from github_navigator import settings


def create_app(config):
    app = Flask(__name__)

    if config:
        app.config.from_object(getattr(settings, config))

    # configure your app...
    return app
