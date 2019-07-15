#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: models.py 
@time: 2018/9/18 0018 19:43 
"""

import enum
from datetime import datetime
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKOWN = 4

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    # 用户id设置自增长的话容易被人猜出用户数量,使用生成随机数的方式，同时呢避免id重复
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    username = db.Column(db.String(50), nullable=False)
    tel = db.Column(db.String(11), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))  # 真实姓名
    avatar = db.Column(db.String(100))  # 头像
    signature = db.Column(db.String(100))  # 个性签名
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKOWN)
    is_display = db.Column(db.Integer, default=1, comment='默认1允许用户发帖,0表示不允许用户发帖')
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpad):
        self._password = generate_password_hash(newpad)

    def check_password(self, rawpwd):
        result = check_password_hash(self.password, rawpwd)
        return result
