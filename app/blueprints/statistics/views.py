# coding: utf-8

from flask import (
    abort,
    request,
    jsonify,
)

from app.services import statistics as stat_services
import app.exceptions as exc
from app.serializers import (
    StatSerializer,
)

from . import statistics


@statistics.route('/', methods=['GET', 'POST'])
def show_stat():
    try:
        stat = stat_services.get_stat(request.json)
    except (exc.InvalidInputData, exc.UserNotFound) as e:
        abort(400, e)
    data, errors = StatSerializer().dump(stat)
    return jsonify(data)
