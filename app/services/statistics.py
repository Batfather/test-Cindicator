# coding: utf-8

from sqlalchemy.sql import func

from voluptuous import (
    Schema,
    Required,
    MultipleInvalid,
)

from ..models import (
    Poll,
    Vote,
)
from .. import db
from .. import exceptions as exc

stat_schema = Schema({
    Required('poll_id'): int,
})


def get_stat(args):
    try:
        data = stat_schema(args)
    except MultipleInvalid as e:
        raise exc.InvalidInputData(e)

    votes = Vote.query.filter(Poll.id == data['poll_id']).all()
    if len(votes) == 0:
        raise exc.NoVotesForPoll('there are no votes for this poll')

    result = {"poll": data['poll_id'],
              "answers": []}
    answers = set([vote.answer_id for vote in votes])

    for answer in answers:
        # Counting average value for every answer.
        avg = db.session.query(func.count(Vote.answer_id)).filter(Vote.answer_id == answer).scalar() / len(votes)
        result["answers"].append({"answer": answer,
                                  "freq": round(avg, 2)})

    return result
