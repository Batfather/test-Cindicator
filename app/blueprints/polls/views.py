# coding: utf-8

from sqlalchemy.exc import IntegrityError
from flask import (
    abort,
    request,
    jsonify,
)
from app.services import (
    polls as polls_services,
    users as users_service,
)
import app.exceptions as exc
from app.serializers import (
    PollSerializer,
    VoteSerializer,
)

from . import polls


@polls.route('/', methods=['POST'])
def create():
    try:
        user = users_service.get_by_token(request.args['token'])
    except exc.UserNotFound as e:
        abort(404, e)

    try:
        poll = polls_services.create_poll(user, request.json)
    except (exc.InvalidInputData, exc.UserNotFound) as e:
        abort(400, e)
    data, errors = PollSerializer().dump(poll)
    return jsonify(data)


@polls.route('/<int:poll_id>/vote/', methods=['GET', 'POST'])
def vote(poll_id):
    try:
        vote = polls_services.create_vote(request.json, poll_id)
    except (exc.InvalidInputData, exc.UserNotFound, exc.PollNotFound, exc.PollOutdated, exc.AnswerNotFound) as e:
        abort(400, e)
    except IntegrityError:
        abort(400, 'You have already voted for this poll')
    data, errors = VoteSerializer().dump(vote)
    return jsonify(data)
