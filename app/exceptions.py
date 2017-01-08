# coding: utf-8


class InvalidInputData(Exception):
    pass


class UserNotFound(Exception):
    pass


class PollOutdated(Exception):
    pass


class PollNotFound(Exception):
    pass


class AnswerNotFound(Exception):
    pass


class NoVotesForPoll(Exception):
    pass


class IncorrectCredentials(Exception):
    pass
