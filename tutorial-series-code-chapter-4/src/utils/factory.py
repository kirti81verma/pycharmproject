import flask_excel as excel
from flask import Flask
from flask.json import JSONEncoder
from .models import db


def create_app(package_name, config, blueprints=None, extensions=None):
    app = Flask(package_name)
    app.config.from_object(config)
    config.init_app(app)
    if blueprints:
        for bp in blueprints:
            app.register_blueprint(bp)
    if extensions:
        for extension in extensions:
            extension.init_app(app)
        excel.init_excel(app)
    
    # if extensions:
    #     for extension in extensions:
    #
    #         extension.init_app(app)

    return app
