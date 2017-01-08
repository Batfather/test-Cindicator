# coding: utf-8

from flask import Blueprint

statistics = Blueprint('statistics', __name__)

from . import views
