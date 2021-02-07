import hashlib
from flask import jsonify, request

class ApiUtils:
    def init_app(self, app):
        self._app = app
        return self
    def make_response_ok(self, data=None):
        resp = {'code': 0, 'msg': 'success'}
        if data:
            resp['data'] = data
        return jsonify(resp)

    def make_response_error(self, code, msg):
        resp = {'code': code, 'msg': msg}
        return jsonify(resp)

    def validsign(self):
        def decorator(func):
            def wrapper():
                params = self.get_request_params()
                appkey = params.get('appkey')
                if not appkey:
                    return self.make_response_error(-1, 'appkey 为空.')
                sign = params.get('sign')
                csign = self._signature(params)
                if not sign or not csign:
                    return self.make_response_error(-1, '签名错误.')
                if csign != sign:
                    if self._app.config['DEBUG']:
                        print(f'[DEBUG]:{csign}--{sign}')
                        return func()
                    return self.make_response_error(-1, '签名错误.')
                return func()

            return wrapper

        return decorator

    def _signature(self, params: dict):
        commons = ['timestamp', 'nonce', 'appkey', 'sign', 'token']
        m = hashlib.md5()
        lst = [f"{k}={v}" for k, v in params.items() if k not in commons]
        lst.sort()
        msg = '&'.join(lst)
        token = params.get('token', '')
        timestamp = params.get('timestamp', '')
        nonce = params.get('nonce')
        appkey = params.get('appkey', '')
        appsecret = self._get_app_secret(appkey)
        if appsecret is None:
            return None
        signBase = f'{msg}{token}{timestamp}{nonce}{appsecret}'.encode('utf-8')
        m.update(signBase)
        return m.hexdigest()

    def _get_app_secret(self, appkey: str):
        key = self._app.config['OPEN_APP_LIST']['appkey']
        if appkey == key:
            return self._app.config['OPEN_APP_LIST']['appsecret']
        return None

    def get_request_param(self, key):
        value = request.form.get(key)
        if not value:
            value = request.args.get(key)
        return value

    def get_request_params(self):
        params = request.form
        if not params:
            params = request.args
        return params