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

from flask import (
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g
)
from flask_paginate import Pagination, get_page_parameter

from apps.front.models import FrontUser
from config import SESSION_USER_ID, PER_PAGE
from exts import db
from utils import restful
from .decoratos import login_required, permission_required
from .forms import (
    LoginForm,
    ResetPwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
    AddCuserrForm,
    UpdateCuserrForm
)
from .models import CMSUser, CMSPermission, CMSRole
from ..models import BannerModel, BoardModel, PostModel, HighlightPostModel, CommentModel, HighlightCommentModel

bp = Blueprint('cms', __name__, url_prefix='/cms')


# 后台首页
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cms/cms_index.html')


# 登录
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user.is_display != 1:
                return self.get(message='对不起,您的账户已被禁用,如有疑问,请联系管理员~~~')
            if user and user.check_password(password):
                # 单独把用户session数据提出来作为一个常量，方便其他代码使用，比如用来验证是否登录的装饰器
                session[SESSION_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            # 根据返回值来操作
            """
            form.errors.popitem()是从字典中随机取出一条数据，返回的是一个元组,比如：('password', ['请输入6-10位密码'])
            需要的是返回的元组中第二个数据，也就是[1],
            又因为元组的第二个数据是一个列表，所以再取列表的第一个数据，也就是[0]
            综合以上分析，所以取出返回的错误信息为form.errors.popitem()[1][0]
            """
            message = form.errors.popitem()[1][0]
            # 对上面的进一步优化，多个类视图函数使用这个，单独抽取出来放到父模型中
            # message = form.get_error()
            return self.get(message=message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 注销
@bp.route('/logout/')
@login_required
def logout():
    # del session[SESSION_USER_ID]
    session.clear()
    return redirect(url_for('cms.login'))


# 修改密码
class ResetPwdView(views.MethodView):
    # 类视图中使用装饰器,登录
    decorators = [login_required]

    def get(self, message=None):
        return render_template('cms/cms_resetpwd.html', message=message)

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            old_password = form.old_password.data
            new_password = form.new_password.data
            user = g.cms_user
            if user.check_password(old_password):
                user.password = new_password
                db.session.commit()
                # 返回给js的字典格式 {'code':200,'message':'密码错误'}
                return restful.success('密码修改成功!')
            else:
                return restful.params_error("原密码错误!")
        else:
            # message = form.get_error()
            # return self.get(message=message)
            return restful.params_error(form.get_error())


bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))


# 修改邮箱
class ResetEmailView(views.MethodView):
    # 类视图中使用装饰器,登录
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


# 测试发送邮件函数
# @bp.route('/email/')
# def send_email():
#     message = Message(subject='发送邮件测试',recipients=['sandu12345@msn.cn','service@ejubei.cn'],
#                       body='使用阿里云企业邮箱发送邮件测试')
#     mail.send(message)
#     return 'success'


# 帖子管理
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    posts = PostModel.query.filter_by(is_display=1).order_by(PostModel.create_time.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=PostModel.query.count())
    content = {
        'posts': posts,
        'pagination': pagination,
    }
    return render_template('cms/cms_posts.html', **content)


# 帖子加精
@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


# 帖子取消加精
@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


# 删除帖子
@bp.route('/dpost/', methods=['POST'])
@permission_required(CMSPermission.POSTER)
@login_required
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入要删除的帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这个帖子')
    post.is_display = '0'
    db.session.commit()
    return restful.success()


# 评论管理
@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    comments_mods = CommentModel.query.order_by(CommentModel.create_time.desc()).slice(start,
                                                                                       end).all()
    pagination = Pagination(bs_version=3, page=page, total=CommentModel.query.count())
    content = {
        'comments_mods': comments_mods,
        'pagination': pagination,
    }

    return render_template('cms/cms_comments.html', **content)


# 评论置顶
@bp.route('/hcomment/', methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def hcomment():
    comment_id = request.form.get("comment_id")
    if not comment_id:
        return restful.params_error('请传入评论id！')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error("没有该评论！")

    highlight = HighlightCommentModel()
    highlight.comment = comment
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


# 评论取消置顶
@bp.route('/uhcomment/', methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def uhcomment():
    comment_id = request.form.get("comment_id")
    if not comment_id:
        return restful.params_error('请传入评论id！')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error("没有该评论！")

    highlight = HighlightCommentModel.query.filter_by(comment_id=comment_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


# 删除(隐藏)评论
@bp.route('/dcomments/', methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def dcomments():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.params_error(message='请传入要删除的评论id')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error(message='没有这个帖子')
    comment.is_display = '0'
    db.session.commit()
    return restful.success()


# 恢复(显示)评论
@bp.route('/udcomments/', methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def udcomments():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.params_error(message='请传入要删除的评论id')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error(message='没有这个帖子')
    comment.is_display = '1'
    db.session.commit()
    return restful.success()


# 版块管理
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    boards_mod = BoardModel.query.order_by(BoardModel.create_time.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=BoardModel.query.count())

    # 统计每个帖子的数量,查出每个版块的id，然后根据id统计出有多少个帖子
    nums = {}
    for x in boards_mod:
        nums[x.id] = len(x.posts)

    context = {
        'boards': boards_mod,
        'pagination': pagination,
        'nums': nums,
    }
    return render_template('cms/cms_boards.html', **context)


# 添加新版块
@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# 修改版块
@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个版块')
    else:
        return restful.params_error(message=form.get_error())


# 删除版块
@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
@login_required
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请传入板块ID')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


# 前台用户管理
@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    fusers = FrontUser.query.order_by(FrontUser.join_time.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=FrontUser.query.count())

    context = {
        'fusers': fusers,
        'pagination': pagination,
    }
    return render_template('cms/cms_fusers.html', **context)


# 允许用户发帖
@bp.route('/hfuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def hfuser():
    fuser_id = request.form.get("fuser_id")
    if not fuser_id:
        return restful.params_error('请传入用户id！')
    fuser = FrontUser.query.filter_by(id=fuser_id).first()
    if not fuser:
        return restful.params_error("没有这个用户！")

    fuser.is_display = 1
    db.session.add(fuser)
    db.session.commit()
    return restful.success()


# 禁止用户发帖
@bp.route('/uhfuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.FRONTUSER)
def uhfuser():
    fuser_id = request.form.get("fuser_id")
    if not fuser_id:
        return restful.params_error('请传入用户id！')
    fuser = FrontUser.query.filter_by(id=fuser_id).first()
    if not fuser:
        return restful.params_error("没有这个用户！")

    fuser.is_display = 0
    db.session.add(fuser)
    db.session.commit()
    return restful.success()


# CMS用户管理
@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    cusers = CMSUser.query.order_by(CMSUser.join_time.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=CMSUser.query.count())

    # 根据用户id查找到用户角色，构造成一个字典
    cms_role = {}
    # print(cusers) # [<CMSUser 4>, <CMSUser 5>]
    for user_id in cusers:
        # print(user_id) # <CMSUser 4>,<CMSUser 5>
        for role_id in user_id.roles:
            # print(user_id.roles) # [<CMSRole 4>,<CMSRole 3>]
            # print(role_id) # <CMSRole 4>,<CMSRole 3>
            # print(role_id.name) # 开发者,管理员
            cms_role[user_id.id] = role_id.name

    roles = CMSRole.query.all()



    context = {
        'cusers': cusers,
        'pagination': pagination,
        'cms_role': cms_role,
        'roles': roles,
    }

    return render_template('cms/cms_cusers.html', **context)


# 添加CMS后台用户
@bp.route('/acusers/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def acusers():
    form = AddCuserrForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data  # role_id
        cusers = CMSUser(username=name, email=email, password=password)
        cuser_role = CMSRole.query.filter_by(id=role).first()
        cuser_role.users.append(cusers)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


# 修改CMS后台用户
@bp.route('/ucusers/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def ucusers():
    # return '功能暂未实现'
    form = UpdateCuserrForm(request.form)
    if form.validate():
        cuser_id = form.cuser_id.data # 传递过来的用户id 11
        role_id = form.role.data # 修改后的用户角色 4
        cusers = CMSUser.query.filter_by(id=cuser_id).first() # 查找该用户
        roles = CMSRole.query.filter_by(id=role_id).first() # 查找该用户对应的角色
        if cusers:
            # 删除原先的用户-角色关系数据
            for tmp in cusers.roles:
                cusers.roles.remove(tmp)
                db.session.commit()
            # 再重新添加一条用户-角色关系数据
            cusers.roles.append(roles)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有找到该用户~~~')
    else:
        return restful.params_error(form.get_error())


# 允许后台用户登录
@bp.route('/hcuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def hcuser():
    cuser_id = request.form.get("cuser_id")
    if not cuser_id:
        return restful.params_error('请传入用户id！')
    cuser = CMSUser.query.filter_by(id=cuser_id).first()
    if not cuser:
        return restful.params_error("没有这个用户！")

    cuser.is_display = '1'
    db.session.add(cuser)
    db.session.commit()
    return restful.success()


# 禁止后台用户登录
@bp.route('/uhcuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def uhcuser():
    cuser_id = request.form.get("cuser_id")
    if not cuser_id:
        return restful.params_error('请传入用户id！')
    cuser = CMSUser.query.filter_by(id=cuser_id).first()
    if not cuser:
        return restful.params_error("没有这个用户！")

    cuser.is_display = '0'
    db.session.add(cuser)
    db.session.commit()
    return restful.success()


# CMS组管理
@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    cms_croles = CMSRole.query.order_by(CMSRole.create_time.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=CMSRole.query.count())

    # tmp_roles = CMSRole.query.group_by(CMSRole.cms_role_id).count()
    # print(tmp_roles)


    context = {
        'pagination': pagination,
        'cms_croles': cms_croles,

    }

    return render_template('cms/cms_croles.html', **context)


# 轮播图管理
@bp.route('/banners/')
@login_required
def banners():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).slice(start, end).all()
    pagination = Pagination(bs_version=3, page=page, total=BannerModel.query.count())
    content = {
        'banners': banners,
        'pagination': pagination,
    }
    return render_template('cms/cms_banners.html', **content)


# 添加轮播图
@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


# 修改轮播图
@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图')
    else:
        return restful.params_error(form.get_error())


# 删除轮播图
@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图ID')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()
