import re, datetime
import flask_login as fl
from flask import Blueprint, request, jsonify, current_app
from app.ApiUtils import *
from app.models import User

_login_manager = fl.LoginManager()
_authDB = None
_app = None
_globalCache = {}# 定义全局缓存区
_auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
_pattern_phone = "(\\+[0-9]+[\\- \\.]*)?(\\([0-9]+\\)[\\- \\.]*)?([0-9][0-9\\- \\.]+[0-9])"
_pattern_email = "[a-zA-Z0-9\\+\\.\\_\\%\\-\\+]{1,256}\\@[a-zA-Z0-9][a-zA-Z0-9\\-]{0,64}(\\.[a-zA-Z0-9][a-zA-Z0-9\\-]{0,25})+"

def init_app(app, db):
    global _app, _authDB
    _app = app
    _authDB = db
    _login_manager.init_app(_app)
    _app.register_blueprint(_auth_bp)

@_auth_bp.route('/login', methods=['POST'], endpoint='login')
@validsign()
def login():
    global _authDB
    current_app.logger.info('login----')
    phone = request.form.get('phone')
    code = request.form.get('code')
    key = f'{phone}-{code}'
    sms_code = _globalCache.get(key)
    if sms_code is None or sms_code != code:
        return make_response_error(-1, 'sms code error')

    user_info = _authDB.session.query(User).filter(User.phone == phone).first()
    if user_info is None:
        user_info = _regist_by_phone(phone)
    fl.login_user(user_info)
    del _globalCache[key]
    return make_response_ok({
        'user_id': user_info.id
    })

@_auth_bp.route('/sendsms', methods=['POST'], endpoint='sendsms')
@validsign()
def sendSMS():
    phone = request.form.get('phone')
    if not re.match(_pattern_phone, phone):
       make_response_error(-1, '手机号格式有误！')
    code = '9527'
    key = f'{phone}-{code}'
    _globalCache[key]=code
    return make_response_ok({'phone': phone, 'code':code})

@_auth_bp.route('/userInfo', methods=['GET'], endpoint='userInfo')
@fl.login_required
@validsign()
def userInfo():
    return make_response_ok({
        'user_id': fl.current_user.id,
        'username': fl.current_user.username,
        'email': fl.current_user.email
    })


@_auth_bp.route('/logout', methods=['GET'], endpoint='logout')
@validsign()
def logout():
    fl.logout_user()
    return jsonify({'code': 0, 'msg':'注销成功'})


def _regist_by_phone(phone):
    global _authDB
    user = User(
        phone=phone,
        username=f'u-{phone}',
        authority=1,
        registerTime=datetime.datetime.now(),
        lastAccessTime=datetime.datetime.now()
    )
    _authDB.session.add_all([user])
    _authDB.session.commit()
    return user

@_login_manager.user_loader
def user_loader(userID):
    global _authDB
    user_info = _authDB.session.query(User).filter(User.id == userID).first()
    if user_info is None:
        return
    return user_info

@_login_manager.request_loader
def request_loader(request):
    print('request_loader...is None')
    return

@_login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({'code': -1, 'msg':'Unauthorized'})