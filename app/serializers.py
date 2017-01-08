# coding: utf-8

from marshmallow import (
    Schema,
    fields,
)


class UserSerializer(Schema):

    class Meta:
        fields = (
            'username',
            'date_created',
        )


class PollSerializer(Schema):
    answers = fields.Nested('AnswerSerializer', many=True)

    class Meta:
        fields = (
            'id',
            'question',
            'answers',
            'date_created',
            'date_finished',
            'date_created',
        )


class AnswerSerializer(Schema):
    class Meta:
        fields = (
            'id',
            'text',
            'date_created',
        )


class VoteSerializer(Schema):
    user = fields.Nested('UserSerializer')
    answer = fields.Nested('AnswerSerializer')
    poll = fields.Nested('PollSerializer')

    class Meta:
        fields = (
            'user',
            'answer',
            'poll',
            'date_created',
        )


class StatSerializer(Schema):
    class Meta:
        fields = (
            'poll',
            'answers',
        )
