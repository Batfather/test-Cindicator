# coding: utf-8

from flask import Blueprint

polls = Blueprint('polls', __name__)

from . import views
