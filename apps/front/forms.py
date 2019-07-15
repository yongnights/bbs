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

from wtforms import StringField,IntegerField
from wtforms import ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo, Regexp

from utils import zlcache
from ..forms import BaseForm


class SignUpForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    email_captcha = StringField(
        validators=[Length(min=6, max=6, message='请输入正确长度的验证码'), InputRequired(message='请输入邮箱验证码!')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的新密码')])
    repeat_password = StringField(validators=[EqualTo("password", message='确认密码必须和新密码保持一致')])
    graph_captcha = StringField(
        validators=[Regexp(r"\w{4}", message='图形验证码错误,请重新输入!'), InputRequired(message='请输入图形验证码!')])

    def validate_email_captcha(self, field):
        captcha = field.data  # 获取用户输入的邮箱验证码
        email = self.email.data  # 获取用户输入的邮箱
        captcha_cache = zlcache.get(email)  # 从缓存中获取发送给用户的邮箱验证码
        if not captcha_cache or captcha.lower() != captcha_cache.lower():  # 验证用户输入的邮箱验证码
            raise ValidationError('邮箱验证码错误!')

    def validate_graph_captcha(self, field):
        captcha = field.data
        captcha_cache = zlcache.get('graph_captcha')
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('图形验证码错误!')


class SigninForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱!')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    graph_captcha = StringField(
        validators=[Regexp(r"\w{4}", message='图形验证码错误,请重新输入!'), InputRequired(message='请输入图形验证码!')])
    remeber = StringField()

    def validate_graph_captcha(self, field):
        captcha = field.data
        captcha_cache = zlcache.get('graph_captcha')
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('图形验证码错误!')

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入新帖子名称!')])
    content = StringField(validators=[InputRequired(message='请输入新帖子内容!')])
    board_id = IntegerField(validators=[InputRequired(message='请输入新帖子所属版块id!')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容!')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id!')])
