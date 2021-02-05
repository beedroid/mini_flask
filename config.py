import os

basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dqwecf29vbneuirjnf2i3n0f2i302n'
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 是否显示修改回执
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 是否自动提交sql执行

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123123@127.0.0.1:3306/economy?charset=utf8'


class TestingConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev:4mmeX({z6P2U8]N[@127.0.0.1:3306/economy?charset=utf8'


class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev:4mmeX({z6P2U8]N[@127.0.0.1:3306/economy?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
