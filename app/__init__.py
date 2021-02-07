import sys, os
from flask import Flask
from config import config
from app.models import db
from app.Auth import init_app as auth_init_app
from app.ApiHandler import api_handler_init_app

currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append((os.path.abspath(os.path.join(currentPath, ".."))))
app = Flask(__name__)
app.secret_key = '123'

config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])  # 导入对应的配置
config[config_name].init_app(app)  # 初始化app配置

db.init_app(app)

auth_init_app(app, db)
api_handler_init_app(app, db)

@app.route('/')
def hello_world():
    return 'Hello World!'




