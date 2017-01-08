# coding: utf-8

from datetime import datetime
from sqlalchemy.schema import UniqueConstraint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class RoleEnum:
    ADMIN = 1
    REGULAR = 2


class User(BaseModel, db.Model):
    __tablename__ = 'user'

    username = db.Column(db.Unicode(100), nullable=False, unique=True, index=True)
    role = db.Column(db.Integer, default=RoleEnum.REGULAR)

    polls = db.relationship('Poll', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    def generate_token(self, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'id': self.id}).decode('utf-8')

    def __repr__(self):
        return u'<User {username}>'.format(username=self.username)


class Poll(BaseModel, db.Model):
    __tablename__ = 'poll'

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.UnicodeText, nullable=False)
    date_started = db.Column(db.DateTime, nullable=False)
    date_finished = db.Column(db.DateTime, nullable=False)

    answers = db.relationship('Answer', backref='poll', lazy='dynamic')
    votes = db.relationship('Vote', backref='poll', lazy='dynamic')

    def __init__(self, author, question, date_started, date_finished):
        self.author = author
        self.question = question
        self.date_started = date_started
        self.date_finished = date_finished

    def __repr__(self):
        return u'<Poll {id}>'.format(id=self.id)


class Answer(BaseModel, db.Model):
    __tablename__ = 'answer'

    text = db.Column(db.Unicode(100), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))

    votes = db.relationship('Vote', backref='answer', lazy='dynamic')

    def __init__(self, text, poll):
        self.text = text
        self.poll_id = poll

    def __repr__(self):
        return u'<Answer {id}>'.format(id=self.id)


class Vote(BaseModel, db.Model):
    __tablename__ = 'vote'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    UniqueConstraint(user_id, poll_id, name='uix_1')

    def __init__(self, author, answer, poll):
        self.user_id = author
        self.answer_id = answer
        self.poll_id = poll
