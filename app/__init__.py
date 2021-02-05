import sys, os, datetime, time
from flask import Flask, session, g, jsonify, redirect, request, flash, url_for, abort
from config import config
import flask_login
from flask_sqlalchemy import SQLAlchemy

currentPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append((os.path.abspath(os.path.join(currentPath, ".."))))
app = Flask(__name__)
db = SQLAlchemy()
db.init_app(app)
app.secret_key = '123'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])  # 导入对应的配置
config[config_name].init_app(app)  # 初始化app配置

users = {'foo@bar.tld': {'password': 'secret'}}


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'mini_flask_user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String)
    userPassword = db.Column(db.String)
    userNickName = db.Column(db.String)
    userAvatar = db.Column(db.String)
    ssoID = db.Column(db.Integer)
    registerTime = db.Column(db.Integer)
    lastAccessTime = db.Column(db.Integer)
    fullOrgName = db.Column(db.Integer)

    def __init__(self, id):
        self.id = id
        self.name = ""


@login_manager.user_loader
def user_loader(userID):
    users = db.session.query(User).filter(User.id == userID)
    if users is None:
        return
    user = users.first()
    if user is None:
        return
    return


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    users = db.session.query(User).filter(User.userName == username)
    if users is None:
        return
    user = users.first()
    if user is None:
        return
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form.get('password') == user.userPassword
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({'code': -1, 'msg':'请使用post请求'})
    username = request.form.get('username')
    users = db.session.query(User).filter(User.userName == username)
    if users is None:
        return jsonify({'code': -1, 'msg': '用户未找到'})
    user = users.first()
    if user is None:
        return jsonify({'code': -1, 'msg':'用户未找到'})
    password = request.form.get('password')
    if password == user.userPassword:
        flask_login.login_user(user)
        return jsonify({'code': 0, 'msg':'登录成功'})
    else:
        return jsonify({'code': -1, 'msg':'密码错误'})
    return jsonify({'code': -1, 'msg':'登录失败'})


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.userName


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return jsonify({'code': 0, 'msg':'注销成功'})


# provide a callback for login failures:
@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({'code': -1, 'msg':'Unauthorized'})


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

# @app.before_request
# def load_current_user():
#     g.user = None
#     if 'openid' in session:
#         g.user = User.query.filter_by(openid=session['openid']).first()

@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}


@app.route('/into')
def into():
    print(g.user)
    return jsonify({'code': 1})