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
from flask import session,g
from config import SESSION_USER_ID
from .models import CMSUser,CMSPermission

@bp.before_request
def before_request():
    if SESSION_USER_ID in session:
        user_id = session.get(SESSION_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_processor():
    return {"CMSPermission": CMSPermission}

