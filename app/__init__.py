# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    from .blueprints.polls import polls as polls_blueprint
    app.register_blueprint(polls_blueprint, url_prefix='/polls')

    from .blueprints.statistics import statistics as stat_blueprint
    app.register_blueprint(stat_blueprint, url_prefix='/stat')

    from .blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    db.init_app(app)

    return app
