#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: forms.py 
@time: 2018/9/18 0018 19:44 
""" 

from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(min=5,max=10,message='请输入6-10位密码'),InputRequired(message='请输入密码')])
    remember = IntegerField()

class ResetPwdForm(BaseForm):
    old_password = StringField(validators=[Length(6, 20, message='请输入正确格式的旧密码')])
    new_password = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码')])
    confirm_new_password = StringField(validators=[EqualTo("new_password", message='确认密码必须和新密码保持一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码'),InputRequired(message='请输入验证码')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache =  zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self,filed):
        email = filed.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图链接地址')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接地址')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图id')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])


class AddCuserrForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入用户姓名')])
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(min=5, max=10, message='请输入6-10位密码'), InputRequired(message='请输入密码')])
    role = IntegerField(validators=[InputRequired(message='请输入用户角色')])

class UpdateCuserrForm(BaseForm):
    cuser_id = IntegerField(validators=[InputRequired(message='请输入用户id')])
    name = StringField(validators=[InputRequired(message='请输入用户姓名')])
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    role = IntegerField(validators=[InputRequired(message='请输入用户角色')])