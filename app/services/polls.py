# coding: utf-8

from datetime import datetime

from voluptuous import (
    Schema,
    Required,
    MultipleInvalid,
)

from . import users as users_service

from ..models import (
    Poll,
    Answer,
    Vote
)
from .. import db
from .. import exceptions as exc


def to_date(fmt='%Y-%m-%d'):
    return lambda v: datetime.strptime(v, fmt).date()

poll_schema = Schema({
    Required('question'): str,
    Required('answers'): [str],
    Required('date_started'): to_date(),
    Required('date_finished'): to_date(),
})

vote_schema = Schema({
    Required('user_id'): int,
    Required('answer_id'): int,
})


def create_poll(user, args):
    try:
        data = poll_schema(args)
    except MultipleInvalid as e:
        raise exc.InvalidInputData(e)

    poll = Poll(user, data['question'], data['date_started'], data['date_finished'])
    db.session.add(poll)
    db.session.flush()

    for answer in data['answers']:
        poll.answers.append(Answer(text=answer, poll=poll.id))

    db.session.commit()

    return poll


def create_vote(args, poll_id):
    try:
        data = vote_schema(args)
    except MultipleInvalid as e:
        raise exc.InvalidInputData(e)

    author = users_service.get_user(data['user_id'])
    if author is None:
        raise exc.UserNotFound('user is not found')

    answer = Answer.query.filter(Answer.id == data['answer_id']).first()
    if answer is None:
        raise exc.AnswerNotFound('answer is not found')

    poll = Poll.query.filter(Poll.id == answer.poll_id).first()
    if poll is None:
        raise exc.PollNotFound('poll is not found')
    if poll.date_started > datetime.now() or poll.date_finished < datetime.now():
        raise exc.PollOutdated('voting has ended or not started for this poll')

    vote = Vote(author.id, data['answer_id'], poll_id)

    db.session.add(vote)
    db.session.commit()

    return vote
