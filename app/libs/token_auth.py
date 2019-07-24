from collections import namedtuple
from app import get_logger

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

__author__ = 'jeellee'

log = get_logger(__name__)
auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    # token
    # HTTP 账号密码
    # header key:value
    # account  qiyue
    # 123456
    # key=Authorization
    # value =basic base64(qiyue:123456)

    log.info('00000000000 %s' % request.headers)
    log.info('1111111111 %s' % token)
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # request
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request 视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)


def get_mina_openid(mina_code):
    """根据code获取微信openid

    :param mina_code: 前端给的code
    :return: openid
    """

    wx_url = current_app.config["WX_URL"].format(
        current_app.config["APP_ID"],
        current_app.config["APP_SECRET"],
        mina_code)
    import json
    from urllib.request import urlopen
    res = urlopen(wx_url, timeout=3)
    res = res.read().decode()
    res = json.loads(res)
    log.info('get_mina_openid: res is %s' % res)
    if "errcode" in res:
        raise AuthFailed(
            msg='get openid error, code: %s' % res.get("errcode", ""),
            error_code=1003)
    # {"errcode":40029,"errmsg":"invalid code,
    #  hints: [ req_id: SwhzmA0599hb31 ]"}
    # {'session_key': 'pwNqx+Mk789WQ5WmA2XFWA==',
    #  'openid': 'oOov64ntscl488S88e8DAqxwD69o'}
    # res = {'session_key': 'pwNqx+Mk789WQ5WmA2XFWA==',
    #        'openid': 'oOov64ntscl488S88e8DAqxwD69o'}
    return res.get("openid")
