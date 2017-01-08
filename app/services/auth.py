# coding: utf-8

from voluptuous import (
    Schema,
    Required,
)

from flask import current_app

from . import users as users_service
from ..models import (
    RoleEnum,
)
from .. import exceptions as exc


schema = Schema({
    Required('user_id'): int,
    Required('password'): str,
})


def get_token(args):
    data = schema(args)

    user = users_service.get_user(data['user_id'])

    if user.role != RoleEnum.ADMIN:
        raise exc.IncorrectCredentials('incorrect credentials')

    if data['password'] != current_app.config['PASSWORD']:
        raise exc.IncorrectCredentials('permission denied')

    return user.generate_token()
