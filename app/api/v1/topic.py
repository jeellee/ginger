# coding: utf-8
from app import get_logger
from flask import g
from flask import request
from app.libs.redprint import Redprint
from app.models.topic import Topic, Vote
from app.models.event import Event
from app.validators.forms import TopicForm, VoteForm
from app.libs.error_code import Success
from flask import jsonify
from app.libs.token_auth import auth

log = get_logger(__name__)
api = Redprint('topic')


@api.route('', methods=['GET'])
@auth.login_required
def index():
    topics = Topic.query.limit(5).all()
    return jsonify(topics)


@api.route('/<int:topic_id>', methods=['GET'])
@auth.login_required
def get_topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first_or_404()
    return jsonify(topic)


@api.route('/vote/<int:topic_id>', methods=['GET'])
@auth.login_required
def get_vote(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first_or_404()
    log.info("topic vote data: %s-%s" % (topic.id, type(topic.id)))
    vote = Vote.query.filter_by(topic_id=topic.id).all()
    return jsonify(vote)


@api.route('/create', methods=['POST'])
@auth.login_required
def create():
    """
    创建一个话题
    :return: 
    """
    uid = g.user.uid
    params = request.get_json(silent=True)
    event_id = params.get("event_id", 1)
    log.info('topic create: params is %s' % params)
    event = Event.query.filter_by(id=event_id).first_or_404()
    # 验证时间是否过期等
    # form = BookSearchForm().validate_for_api()
    form = TopicForm().validate_for_api()
    Topic.create_topic(uid,
                       form.name.data,
                       form.start_time.data,
                       form.end_time.data,
                       form.red_topic.data,
                       form.blue_topic.data,
                       form.bg.data,
                       int(event.id))
    return Success()


@api.route('/vote', methods=['POST'])
@auth.login_required
def vote():
    """
    给话题投票
    :return: 
    """
    uid = g.user.uid
    # form = VoteForm().validate_for_api()
    # topic_id = form.topic_id.data
    # vote_who = form.vote_who.data
    params = request.get_json(silent=True)
    log.info('topic vote: params is %s' % params)
    vote_topic = params.get("vote_topic", 1)
    vote_who = params.get("vote_who", 1)
    topic = Topic.query.filter_by(id=vote_topic).first_or_404()

    # 投票
    Vote.create_vote(uid, vote_who, topic.id)
    return Success()

