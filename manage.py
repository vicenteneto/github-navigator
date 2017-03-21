from flask_script import Server, Manager

from github_navigator.app import create_app
from github_navigator_util.constants import Config

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config',
                   choices=(Config.DEVELOPMENT_CONFIG, Config.PRODUCTION_CONFIG, Config.TESTING_CONFIG),
                   default=Config.DEVELOPMENT_CONFIG)
manager.add_command('runserver', Server(host='0.0.0.0', port=8081, processes=2))

if __name__ == '__main__':
    manager.run()
