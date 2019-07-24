import logging
from flask import request, current_app

from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm, UserMinaForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException


__author__ = '七月'

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    logging.info("create_client: start")
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MINA: __register_user_by_mina,
        }
    promise[form.type.data]()
    logging.info("create_client: end")
    logging.error("create_client: 1111111")
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)


def __register_user_by_mina():
    # 微信登录没有注册步骤
    # 已注册的用户 判断openid有无，可绑定微信openid
    # account = StringField(validators=[DataRequired(message='不允许为空'), length(
    #     min=5, max=32
    # )])
    # secret = StringField()
    # type = IntegerField(validators=[DataRequired()])
    params = request.get_json(silent=True)
    mina_code = params.get("account")

    from app.libs.token_auth import get_mina_openid
    from app.libs.error_code import ServerError
    openid = get_mina_openid(mina_code)
    if User.query.filter_by(openid=openid).first():
        raise ServerError(msg='the current user has been already registered',
                          error_code=1003)
    User.register_by_mina(openid)
