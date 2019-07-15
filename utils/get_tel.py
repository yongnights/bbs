#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: get_tel.py 
@time: 2018-10-09 0009 下午 16:52 
"""

import random


# 随机生成手机号
def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)

# 生成手机号
# phone = create_phone()
# print(phone)
