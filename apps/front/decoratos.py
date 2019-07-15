#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: decoratos.py 
@time: 2018-09-20 0020 下午 17:02 
"""
from flask import session,redirect,url_for,g
from functools import wraps
from config import SESSION_FRONT_ID

def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if SESSION_FRONT_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner


