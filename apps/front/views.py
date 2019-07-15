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

import random
import string
from io import BytesIO

from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
    request,
    url_for,
    session,
    redirect,
    g,
    abort,
)
from flask_mail import Message

from exts import db, mail
from utils import restful, zlcache, get_tel, safeutils
from utils.captcha import Captcha
from .forms import SignUpForm,SigninForm,AddPostForm,AddCommentForm
from .models import FrontUser
from config import SESSION_FRONT_ID,PER_PAGE
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel
from .decoratos import login_required
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy import func


bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get("st",type=int,default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(7)
    boards = BoardModel.query.all()
    start = (page-1) * PER_PAGE
    end = start + PER_PAGE

    if sort == 1:
        query_obj = PostModel.query.filter_by(is_display=1).order_by(PostModel.create_time.desc()).filter_by(is_display=1)
    elif sort == 2:
        # 按照加精的时间倒序排序
        query_obj = db.session.query(PostModel).filter_by(is_display=1).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = PostModel.query.filter_by(is_display=1).order_by(PostModel.create_time.desc())
    else:
        # 按照评论最多排序
        query_obj = db.session.query(PostModel).filter_by(is_display=1).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())


    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()

    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=1)
    context = {
        'banners':banners,
        'boards': boards,
        'posts':posts,
        'pagination':pagination,
        'current_board': board_id,
        'current_sort':sort,
    }

    return render_template('front/front_index.html',**context)


@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    zlcache.set('graph_captcha', text)
    # BytesIO 自截留,二进制流数据
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer  # 获取上一个页面的url
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(
                return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignUpForm(request.form)
        if form.validate():
            email = form.email.data
            user = FrontUser.query.filter_by(email=email).first()
            if user:
                return restful.unauth_error('邮箱地址已存在,请换一个邮箱地址!')
            else:
                user_message = FrontUser(username=email, tel=get_tel.create_phone(), password=form.password.data,
                                         email=form.email.data)
                db.session.add(user_message)
                db.session.commit()
                return restful.success()
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数!')

    source = list(string.ascii_letters)  # 产生a-zA-Z的一个字符串,并转换成列表
    source.extend(map(lambda x: str(x), range(0, 10)))  # 产生0-9的数字，并使用匿名函数转换成字符串，然后增加到source列表中
    captcha = ''.join(random.sample(source, 6))

    message = Message(subject='Python论坛邮箱验证码', recipients=[email],
                      body='您此次注册账号的邮箱验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    zlcache.set(email, captcha)  # 验证码存入到memcache中，有效期60s
    return restful.success()


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html',return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remeber.data
            user = FrontUser.query.filter_by(email=email).first()
            # 判断用户是否允许发帖
            if user.is_display == 0:
                return restful.params_error(message='对不起,您的账户已被禁用,如有疑问,请联系管理员~~~')
            if user and user.check_password(password):
                session[SESSION_FRONT_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='邮箱或密码错误！')
        else:
            return restful.params_error(message=form.get_error())

bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))

@bp.route('/signout/')
@login_required
def signout():
    session.clear()
    return redirect(url_for('front.index'))

# 添加新帖子
@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        context = {
            'boards':boards,
        }
        return render_template('front/front_apost.html',**context)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个版块！')

            post = PostModel(title=title,content=content,board_id=board_id,author_id=session[SESSION_FRONT_ID])
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

# 帖子详情
@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)

    comments = CommentModel.query.filter(db.and_(CommentModel.post_id==post.id,CommentModel.is_display==1)).all()

    content = {
        'post':post,
        'comments':comments
    }
    return render_template('front/front_pdetail.html',**content)

@bp.route('/acomment/',methods = ['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这篇帖子！')
    else:
        return restful.params_error(message=form.get_error())

