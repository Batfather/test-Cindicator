# coding: utf-8

from flask_script import Manager
from flask_script import prompt_bool

from app import db
from app import models
from app import create_app


app = create_app()
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)

@manager.command
def respawn():
    if prompt_bool('Are you sure you want to lose all your data?'):
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    manager.run()
