"""
 Created by 七月 on 2018/5/8.
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token, gift, event, topic

__author__ = '七月'


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    event.api.register(bp_v1)
    topic.api.register(bp_v1)
    return bp_v1
