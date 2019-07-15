#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: exts.py 
@time: 2018/9/18 0018 19:41 
""" 

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayu import AlidayuAPI

db = SQLAlchemy()
mail = Mail()
alidayu = AlidayuAPI()