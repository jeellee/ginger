import os
import sys
import logging
from .app import Flask
__author__ = '七月'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_logger(name):
    logger = logging.getLogger(name)
    log_path = os.path.join(BASE_DIR, "logs")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    # 指定logger输出格式
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - '
                                      '%(filename)s - %(funcName)s - '
                                      '%(lineno)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    # 文件日志
    file_handler = logging.FileHandler("%s/%s" % (log_path, "ginger.log"))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.DEBUG)
    return logger


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)
    register_plugin(app)

    return app

