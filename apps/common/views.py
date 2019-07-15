#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: views.py 
@time: 2018/9/18 0018 19:43 
""" 

from flask import Blueprint,request,jsonify
from exts import alidayu
from utils.captcha import Captcha
from exts import mail
from utils import restful,zlcache
from flask_mail import Message
import string
import random
import qiniu

bp = Blueprint('common',__name__,url_prefix='/common')

@bp.route('/')
def index():
    return 'common index'

@bp.route('/sms_captcha/')
def sms_captcha():
    tel = request.args.get('tel')
    if not tel:
        return restful.params_error(message='请输入手机号码')
    captcha = Captcha.gene_text(number=4)
    result = alidayu.send_sms(tel,code=captcha)
    if result:
        return restful.success()
    else:
        return restful.params_error(message='短信验证码发送失败')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数!')

    source = list(string.ascii_letters) # 产生a-zA-Z的一个字符串,并转换成列表
    source.extend(map(lambda x:str(x),range(0,10))) # 产生0-9的数字，并使用匿名函数转换成字符串，然后增加到source列表中
    # captcha = random.sample(source,6) # 从source列表中随机产生6个字符串组成的列表
    # captcha = ''.join(captcha) # 列表转换成一个字符串
    captcha = ''.join(random.sample(source,6))

    message = Message(subject='Python论坛邮箱验证码',recipients=[email],
                      body='您此次的邮箱验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    zlcache.set(email,captcha) # 验证码存入到memcache中，有效期60s
    return restful.success()

@bp.route('/uptoken/')
def uptoken():
    access_key = 'pKTPqG8HZbSd8ooqtAdLCF6p6_krEDvqNzUni_o7'
    secret_key = '_UlbkZjH50DT_HR0XH1Pm95f_KQGIyn52wnFIJGU'
    q = qiniu.Auth(access_key,secret_key)

    bucket = 'pyhton-flask' # 七牛上创建的存储空间名称
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})