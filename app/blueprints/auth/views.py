# coding: utf-8

from flask import (
    abort,
    request,
    jsonify,
)
from app.services import auth as auth_services
import app.exceptions as exc

from . import auth


@auth.route('/sign-in/', methods=['POST'])
def sign_in():
    try:
        token = auth_services.get_token(request.json)
    except exc.UserNotFound as e:
        abort(400, e)
    except exc.IncorrectCredentials as e:
        abort(403, e)

    return jsonify({'token': token}), 200
