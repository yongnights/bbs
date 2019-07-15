#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: forms.py 
@time: 2018-09-21 0021 上午 11:21 
""" 

from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message