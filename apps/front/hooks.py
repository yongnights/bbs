#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: hooks.py 
@time: 2018-09-20 0020 下午 18:31 
""" 

from .views import bp
from flask import session,g,render_template
from config import SESSION_FRONT_ID
from .models import FrontUser

@bp.before_request
def before_request():
    if SESSION_FRONT_ID in session:
        user_id = session.get(SESSION_FRONT_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user

@bp.errorhandler
def page_not_found():
    return render_template("front/front_404.html"),404