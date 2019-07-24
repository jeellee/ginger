from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

__author__ = 'jeellee'


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    @staticmethod
    def validate_account(value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class UserMinaForm():
    pass

    @staticmethod
    def validate_account(value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


class TopicForm(Form):
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(24), nullable=False)
    focus_users = Column(String(24), default='')
    start_time = Column(Integer, default=0)
    end_time = Column(Integer, default=0)
    red_topic = Column(String(24))
    blue_topic = Column(String(24))
    event = relationship('Event')
    event_id = Column(Integer, ForeignKey('event.id'))
    """
    name = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    start_time = IntegerField(validators=[DataRequired()])
    end_time = IntegerField(validators=[DataRequired()])
    red_topic = StringField(validators=[length(max=20)])
    blue_topic = StringField(validators=[length(max=20)])
    bg = StringField(validators=[length(max=100)])


class EventForm(Form):
    name = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=24
    )])
    type = IntegerField(validators=[DataRequired()])
    create_time = IntegerField(validators=[DataRequired()])
    content = StringField(validators=[DataRequired(message='不允许为空'), length(max=500)])


class VoteForm(Form):
    topic_id = IntegerField(validators=[DataRequired(message='不允许为空'), length(max=1)])
    vote_who = IntegerField(validators=[DataRequired(message='不允许为空'), length(max=1)])
