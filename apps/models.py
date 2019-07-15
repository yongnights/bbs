#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" 
@Project:zhifu
@author:sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: models.py 
@time: 2018-10-11 0011 下午 14:42 
""" 

from exts import db
from datetime import datetime

class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"),nullable=False) # 外键
    author_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    is_display = db.Column(db.String(1),default='1',comment='默认1显示,0表示删除,不显示')

    board = db.relationship("BoardModel",backref="posts") # 外键：一对多，一个版块里可以有多个帖子
    author = db.relationship("FrontUser",backref='posts')

class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    create_time = db.Column(db.DateTime,default=datetime.now)

    post = db.relationship("PostModel",backref="highlight")


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_display = db.Column(db.String(1),default='1',comment='默认1显示,0表示删除,不显示')

    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("front_user.id"),nullable=False)

    post = db.relationship("PostModel",backref="comments")
    author = db.relationship("FrontUser",backref="comments")

class HighlightCommentModel(db.Model):
    __tablename__ = 'highlight_comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment_id = db.Column(db.Integer,db.ForeignKey("comment.id"))
    create_time = db.Column(db.DateTime,default=datetime.now)

    comment = db.relationship("CommentModel",backref="highlight")