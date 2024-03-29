from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm, LargeBinary
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

__author__ = 'jeellee'


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    openid = Column(String(100), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))
    # static = LargeBinary(length=2048)

    def keys(self):
        return ['id', 'email', 'nickname', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def register_by_mina(openid):
        with db.auto_commit():
            user = User()
            user.nickname = openid
            user.openid = openid
            user.email = "wx@%s.com" % openid
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def verify_by_mina(mina_code, password):
        from app.libs.token_auth import get_mina_openid
        openid = get_mina_openid(mina_code)
        # openid = 'aaaaaaaaaaaaaaa'
        user = User.query.filter_by(openid=openid).first_or_404()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']
