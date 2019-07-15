#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Project:zhiliao_flask
@author:DESKTOP-Sandu
@Email: sandu12345@msn.cn
@Software: PyCharm
@file: manage.py 
@time: 2018/9/18 0018 19:41 
""" 

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from run import create_app
from exts import db
from apps.cms.models import CMSUser,CMSRole,CMSPermission
from apps.front.models import FrontUser
from apps.models import BoardModel,PostModel
from utils.get_tel import create_phone


app = create_app()

manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)

# 通过命令添加用户信息
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')


@manager.command
def create_role():
    # 1. 访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='只能相关数据，不能修改。')
    visitor.permissions = CMSPermission.VISITOR

    # 2. 运营角色（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营者',desc='管理帖子，管理评论,管理前台用户。')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

    # 3. 管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 4. 开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s'%role)
    else:
        print('%s邮箱没有这个用户!'%email)

@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.is_developer:
        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者权限！')

# 添加前台用户
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-t','--tel',dest='tel')
def create_front_user(username,password,tel):
    user = FrontUser(username=username,password=password,tel=tel)
    db.session.add(user)
    db.session.commit()
    print('前台用户添加成功')


# 批量添加测试帖子，用来实现分页
@manager.command
def create_test_post():
    for x in range(1,101):
        title = '标题%s' % x
        content = '内容：%s' % x
        board = BoardModel.query.first()
        author = FrontUser.query.first()
        post = PostModel(title=title,content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('恭喜！测试帖子添加成功！')

# 批量添加前台用户，测试分页
@manager.command
def create_fuser_post():
    for x in range(21,40):
        username = '用户%s' % x
        tel = create_phone()
        password = create_phone()
        email = create_phone() + '@qq.com'
        fuser = FrontUser(username=username,tel=tel,password=password,email=email)
        db.session.add(fuser)
        db.session.commit()
    print('恭喜！测试用户添加成功！')


if __name__ == '__main__':
    manager.run()


"""
manage.py db:(choose from 'init', 'revision', 'migrate', 'edit', 'merge', 'upgrade', 
'downgrade', 'show', 'history', 'heads', 'branches', 'current', 'stamp')

1.python manage.py db init
2.python manage.py db migrate
3.python manage.py db upgrade
若修改用户模型则重复步骤2和3
"""