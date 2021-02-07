from flask_sqlalchemy import SQLAlchemy
import datetime
import flask_login

db = SQLAlchemy()


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'mini_flask_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    phone = db.Column(db.String(16))
    email = db.Column(db.String(64))
    gender = db.Column(db.Integer) # 1男2女0未知
    birthday = db.Column(db.DateTime)
    avatar = db.Column(db.String(128))
    emotion = db.Column(db.Integer)  # 情感状态 0 单身 1 已婚 2 离异 3保密
    height = db.Column(db.Integer)
    sexual = db.Column(db.String(2))  # 性取向 1 男 2女 0未知
    education = db.Column(db.String(64))  # 0 未知; 1 高中及以下; 2中专; 3大学; 4硕士; 5 博士
    salary = db.Column(db.Integer)  # 1: 3000以下；2: 3000-5000；3: 5000-8000; 4: 8000-10000; 5: 10000-20000; 6: 20000以上
    authority = db.Column(db.Integer)  # 个人资料可见性（0：所有用户不可见，1：所有用户可见，2：仅我关注的人可见）
    ssoID = db.Column(db.Integer)
    registerTime = db.Column(db.Integer)
    lastAccessTime = db.Column(db.Integer)
    fullOrgName = db.Column(db.Integer)

    def format_birthday(self):
        if isinstance(self.birthday, datetime):
            return self.birthday.strftime('%Y-%m-%d')
        return None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.nickname})'
