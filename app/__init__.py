import sys, os, datetime, time
from flask import Flask, session, g, jsonify, redirect, request, flash, url_for, abort
from config import config
import flask_login
from flask_sqlalchemy import SQLAlchemy

currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append((os.path.abspath(os.path.join(currentPath, ".."))))
app = Flask(__name__)
db = SQLAlchemy()
app.secret_key = '123'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])  # 导入对应的配置
config[config_name].init_app(app)  # 初始化app配置

users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({'code': -1, 'msg':'请使用post请求'})
    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return jsonify({'code': 0, 'msg':'登录成功'})
    return jsonify({'code': -1, 'msg':'登录失败'})


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


# provide a callback for login failures:
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'code' : '-1',
        'msg' : '接口不存在' + str(error)
    })

@app.errorhandler(401)
def not_found(error):
    return jsonify({
        'code' : '-1',
        'msg' : '服务异常：' + str(error)
    })

@app.before_request
def load_current_user():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()

@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}


@app.route('/into')
def into():
    print(g.user)
    return jsonify({'code': 1})