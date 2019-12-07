# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from watermelon import db
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 西瓜预测记录
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String(10))
    time = db.Column(DATETIME(fsp=6), default=datetime.now().replace(microsecond=0), nullable=False)  # 去掉微秒部分
