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

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class CMSPermission():
    # 255的二进制方式来表示 1111 1111
    # 0b表示二进制
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR =        0b00000001
    # 2. 管理帖子权限
    POSTER =         0b00000010
    # 3. 管理评论的权限
    COMMENTER =      0b00000100
    # 4. 管理板块的权限
    BOARDER =        0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER =      0b00010000
    # 6. 管理后台用户的权限
    CMSUSER =        0b00100000
    # 7. 管理后台管理员的权限
    ADMINER =        0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    # _password设置String(50)的话生成的加密密码过长，只有部分保存在数据库中，造成用户登录时账号密码验证失败
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_display = db.Column(db.Integer, default=1, comment='默认1显示,0表示删除,不显示')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    # 判断用户是否属于某个角色以及角色下的权限
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions # 或：all_permissions = all_permissions&permissions
        return all_permissions

    # 判断用户是否有某个权限
    def has_permission(self,permission):
        all_permissions = self.permissions
        return self.permissions&permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)


# user = CMSUser()
# print(user.password)

# user.password = 'abc'

# 密码：对外的字段名叫做password
# 密码：对内的字段名叫做_password


