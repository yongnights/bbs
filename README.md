# bbs
使用flask搭建的一个前后台的BBS论坛

## 安装依赖
pip install -r requirement.txt

## 导入bbs.sql数据库

## 修改config.py文件

修改里面关于数据库的配置信息
修改里面关于邮箱的配置信息

### 数据库(从头开始才使用)
1. 数据库相关操作
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
2. 创建角色模型
python manage.py create_role
3. 添加后台用户
python manage.py create_cms_user -u 111111 -p 111111 -e 111111@111111.com
4. 给后台用户分配角色权限
python manage.py add_user_to_role -e 111111@111111.com -n 访问者


问题：
1. BBS论坛图片已经不显示了，是因为使用的七牛云服务已经停用了

注意：
(1)需要安装memcached和redis

(2)上传轮播图使用七牛云存储
    1.D:\zl_bbs\static\cms\js\banners.js 中修改七牛云的链接
    2.D:\zl_bbs\apps\common\views.py 中uptoken修改七牛云的key信息
    3.js文件中修改qiniuUploadUrls变量值
        D:\zl_bbs\static\cms\js\qiniu_js\qiniu.js
        var qiniuUploadUrls = [
            "http://upload.qiniu.com",
            "http://up.qiniu.com",
        ];

        这个是七牛存储区域，默认的是华东区域不同的存储空间对应的值不同：
        存储区域 	地域简称 	上传域名
        华东 	    z0 	        服务器端上传：http(s)://up.qiniup.com
                                客户端上传： http(s)://upload.qiniup.com
        华北 	    z1 	        服务器端上传：http(s)://up-z1.qiniup.com
                                客户端上传：http(s)://upload-z1.qiniup.com
        华南 	    z2 	        服务器端上传：http(s)://up-z2.qiniup.com
                                客户端上传：http(s)://upload-z2.qiniup.com
        北美 	    na0 	    服务器端上传：http(s)://up-na0.qiniup.com
                                客户端上传：http(s)://upload-na0.qiniup.com
        东南亚 	    as0 	    服务器端上传：http(s)://up-as0.qiniup.com
                                客户端上传：http(s)://upload-as0.qiniup.com

账号信息：
网站：http://blog.frp.lehly.com
前台用户：1103324414@qq.com
密码：111111
注:已无法登录


后台：http://blog.frp.lehly.com/cms
账号：admin@admin.com
密码：444444


问题
1.前台用户点击刷新验证码时刷新不出来，有时候需要整个页面刷新才出来
报错信息：OSError: cannot open resource
解决方法：不采用随机选择字体，而是固定某一种字体
2.后台编辑轮播图，比如修改权重，但是结果却是新增一个一样轮播图，只不过权重不一样
解决方法：核对html中的id或class中的对象等，与js中引用的是否一致，已解决

3.首页已隐藏按点赞数排序，按评论数排序，后续加上

4.评论管理
5.前台用户管理
页面展示已完成，分页已完成，允许/禁止用户发帖  =>已完成
=>首页用户登录检测用户是否有发帖权限，没有权限的话禁止登陆 =>已完成
=>首页用户注销,跳转到首页 =>已完成
=>点击"首页"跳转 =>已完成

前台用户：个人中心，设置

6.cms用户管理

7.后台轮播图加上分页功能 =>已完成
前台轮播图调整到显示7个 =>已完成

8.版块管理加分页功能 =>已完成
版块管理中显示每个版块的帖子数量  =>已完成

9.评论管理
 后台页面展示 =>已完成
 评论置顶/取消置顶 => 创建模型，映射到数据库 :数据库等已完成，还差具体页面评论显示
 限定用户评论数  => 已完成
 删除评论(隐藏)/恢复评论(显示)  =>已完成
 
10.后台管理前台的CMS用户
 后台页面展示
 禁止/恢复用户登录/发帖

11.cms后台用户管理
 页面展示，允许/禁止登录  =>已完成
 添加后台用户 => 已完成
 修改用户权限)  => 已完成
 修改密码 => 该功能交给用户自己修改
 
 遗留问题：编辑用户信息时，用户角色默认显示不是自己的 => 已完成

12.cms组管理
 每个组下面有多少成员，成员名称  => 未完成 (如何构造参数传递过去)
 比如说，开发下面有2人，成员分别是111111和222222，如何根据角色id取出该角色有多少个成员，成员名称是啥
 
 