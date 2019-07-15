#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: config.py 
@time: 2018/9/18 0018 19:41 
"""

from datetime import timedelta
import os

DEBUG = True

# 数据库配置信息
HOSTNAME = '118.25.74.162'
PORT = '3306'
DATABASE = 'zl_bbs'
USERNAME = 'zl_bbs'
PASSWORD = 'zl_bbs'

# dialect+driver://username:password@host:port/database
DB_URI = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(username=USERNAME,
                                                                                           password=PASSWORD,
                                                                                           host=HOSTNAME,
                                                                                           port=PORT,
                                                                                           db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设置session3个小时候过期
PERMANENT_SESSION_LIFETIME = timedelta(hours=3)

#SECRET_KEY = os.urandom(24)
SECRET_KEY = 'abcdferfgg'

# session用户id
SESSION_USER_ID = 'ABCDEabcde1234567890' # 必须是字符串

SESSION_FRONT_ID = 'ABCDEabcde1234567890' # 必须是字符串

# 发送者邮箱配置信息

# QQ邮箱不支持非加密方式发送邮件
# MAIL_USE_TLS协议：端口号587
# MAIL_USE_SSL协议：端口号465

'''
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587' # 默认25端口
MAIL_USE_TLS = True
# MAIL_USE_SSL
# MAIL_DEBUG : default app.debug # debug模式
MAIL_USERNAME = "2413357360@qq.com"
MAIL_PASSWORD = "ghsnqpxaneujdjdg" # QQ邮箱授权码，生成后永久有效，而不是QQ邮箱密码
MAIL_DEFAULT_SENDER = "2413357360@qq.com"
'''

# 使用公司阿里云企业邮箱
MAIL_SERVER = "smtp.mxhichina.com"
MAIL_PORT = '465' # 默认25端口
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug # debug模式
MAIL_USERNAME = "shenqingios@ejubei.cn"
MAIL_PASSWORD = "SHENqing12345" # 企业邮箱密码
MAIL_DEFAULT_SENDER = "shenqingios@ejubei.cn"

# 阿里大于相关配置
ALIDAYU_APP_KEY = '23866570'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_37105566'


##########若七牛云未配置，则上传的图片保存到如下的目录中#############

# 上传的图片保存路径
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')

# ueditor中上传图片到七牛云，如下是七牛云存储的配置，若开启，则图片上传到七牛云上
UEDITOR_UPLOAD_TO_QINIU = False
UEDITOR_QINIU_ACCESS_KEY = "pKTPqG8HZbSd8ooqtAdLCF6p6_krEDvqNzUni_o7"
UEDITOR_QINIU_SECRET_KEY = "_UlbkZjH50DT_HR0XH1Pm95f_KQGIyn52wnFIJGU"
UEDITOR_QINIU_BUCKET_NAME = "pyhton-flask"
UEDITOR_QINIU_DOMAIN = "http://pgmhjjvoy.bkt.clouddn.com/"

# 分页设置，flask_paginate
PER_PAGE = 10


