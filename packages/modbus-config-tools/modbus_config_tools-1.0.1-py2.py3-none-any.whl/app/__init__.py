from app.tool import conf_path
from flask import Flask, render_template,flash
from flask_wtf.csrf import CSRFProtect
import logging
from logging.config import dictConfig
import os
import time
from .settings import Config


def create_conf(conf_path):

    if not os.path.exists(conf_path):
        os.mkdir(conf_path)


def create_log(log_path, log_level):

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            # 'format': '[%(asctime)s] [%(name)-8s] [%(levelname)-8s]: %(filename)s line:%(lineno)d %(message)s',
            'format': '[%(asctime)s]  [%(levelname)-5s]  [%(message)s]',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_path, '{}.log'.format(time.strftime('%Y-%m-%d'))),
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 5,  # 备份数
                'formatter': 'default',  # 输出格式
                'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
            }
        },
        'loggers': {
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            },
            'app': {
                'level': log_level,
                'handlers': ['file']
            }}
    })

    logging.getLogger('log_name')


def create_app(test_config=None):
        # a default secret that should be overridden by instance config
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )
    if test_config is None:

        app.config.from_object('app.settings.DevelopmentConfig')
    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    CSRFProtect(app)
    create_log(Config.log_path, Config.log_level)
    create_conf(Config.conf_path)
    from app import db

    db.init_app(app)
    """
    蓝图注册
    """
    from app import tool,auth
    app.register_blueprint(tool.mt)
    app.register_blueprint(auth.auth)

    @app.route('/', methods=['GET'], endpoint='index')
    def index():
        flash('爱上一个地方，就应该背上包去旅行，走得更远。大家都在等你，还不快过来。。。玩耍！！！', 'success')
        return render_template('index.html', home='bg-primary')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404/page_not_found.html'), 404

    @app.before_first_request
    def before_first():
        app.logger.debug("MT.重新启动")

    app.add_url_rule("/", endpoint="index")

    return app
