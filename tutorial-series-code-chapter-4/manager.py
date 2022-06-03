import os

import urllib.parse as up
from flask_script import Manager
from flask import url_for

from src import db, ma, create_app, configs, api
# from .src.utils import db, configs, BaseMixin, ReprMixin, ma, BaseSchema, create_app, api


config = os.environ.get('PYTH_SRVR', 'default')

config = configs.get(config)

extensions = [db, ma, api]

app = create_app(__name__, config, extensions=extensions)

manager = Manager(app)


@manager.shell
def _shell_context():
    return dict(
        app=app,
        db=db,
        ma=ma,
        config=config
        )


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = up.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)

if __name__ == '__main__':
    manager.run()
