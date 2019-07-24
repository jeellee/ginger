# coding: utf-8
from app import get_logger
from app.libs.redprint import Redprint
from app.models.event import Event
from app.models.base import db
from app.libs.error_code import Success
from flask import jsonify
from app.libs.token_auth import auth
from app.validators.forms import EventForm

log = get_logger(__name__)
api = Redprint('event')


@api.route('/<int:event_id>', methods=['GET'])
@auth.login_required
def get_event(event_id):
    log.info("get_event: %s" % event_id)
    event = Event.query.filter_by(id=event_id).first_or_404()
    log.error("99999999999999999999999999999: %s" % event)
    return jsonify(event)


@api.route('/create', methods=['POST'])
@auth.login_required
def create():
    """
    创建一个事件
    :return: 
    """
    with db.auto_commit():
        event = Event()
        form = EventForm().validate_for_api()
        event.name = form.name.data
        event.type = form.type.data
        event.create_time = form.create_time.data
        event.content = form.content.data
        db.session.add(event)
    return Success()
