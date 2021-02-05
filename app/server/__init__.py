from flask import Blueprint
from flask_restful import Api
from app.server.api.EnvCheckApi import *

# 定义main蓝图
mainBP = Blueprint('main', __name__)
mainApi = Api(mainBP)
mainApi.add_resource(EnvCheckApi, '/env_check', endpoint="env_check")


def init_app(app):
    # 注册蓝本 Flask 使用蓝本来定义路由，在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由真正成为程序的一部分。
    app.register_blueprint(mainBP, url_prefix='/api/main')