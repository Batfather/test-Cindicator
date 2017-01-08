# coding: utf-8

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from itsdangerous import BadSignature

from flask import current_app

from .. import exceptions as exc
from ..models import User


def get_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        raise exc.UserNotFound('user not found')

    return user


def get_by_token(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])

    if token is None:
        raise exc.UserNotFound('user not found')

    try:
        data = serializer.loads(token)
    except (SignatureExpired, BadSignature):
        raise exc.UserNotFound('user not found')

    pk = data.get('id')
    if pk is not None:
        return User.query.filter_by(id=pk).first()
    raise exc.UserNotFound('user not found')
