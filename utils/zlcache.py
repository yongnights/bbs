#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: zlcache.py 
@time: 2018-09-25 0025 下午 19:42 
""" 


import memcache

cache = memcache.Client(['127.0.0.1:11211'],debug=True)

def set(key,value,timeout=60):
    return cache.set(key,value,timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)