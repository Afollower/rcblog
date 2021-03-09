## 个人博客项目
### 1. 基本信息
#### 1.1 开始时间 
2020/12/21
#### 1.2 日程记录
1. 创建项目骨架：2020/12/21 19:55:00 
2. 完成登录注册相关功能： 2020/12/26 17:20:00
3. 2021/1/20完成基础功能；
4. 2021/02/09基础功能完成，并发布到腾讯云服务器上部署方式，Nginx + uwsgi
当前进度：评论模块

### 2. 项目介绍
#### 1. 相关技术栈
Django 2.2 Python3.6 Bootstrap4

#### 2. 项目基础功能
1. 登录管理，借用Django自带后端实现博客增删及相关管理
2. 博客索引界面及博文显示界面
3. 评论留言功能

#### 3. 待完善
1. 前端样式
2. 评论分页
3. 随笔记录

### 3. 系统部署
1. 下载项目
2. 终端运行`pip install -r requirements.txt`，快速安装相关依赖项
3. 数据库迁移：
    ```
    #setting.py 配置数据库依赖
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'POST': '3306',
        }
    }
    
    #终端数据库迁移
    python manage.py makemigrations
    python manage.py migrate
    ```
4. 创建超级管理员
`python manage.py createsuperuser`

5. 尝试运行项目
`python manage.py runserver 0.0.0.0:8000`

6. 尝试访问：http://localhost:8000/index

### 4. 最终效果【未开启评论功能】
http://118.24.124.26:8000/index/