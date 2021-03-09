"""rcblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# 关闭调试后读取静态文件
from django.views import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),

    # 次级目录
    path('', include('homepage.urls')),     # 主页
    path('user/', include('user.urls')),  # 用户

    # Debug = False时用以读取静态文件
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    # 验证码
    path(r'captcha/', include('captcha.urls')),
    # markdown
    path(r'mdeditor/', include('mdeditor.urls')),
    # 设置图片上传显示
    path(r'^uploads/(?P<path>.*)$', static.serve, {"document_root": settings.MEDIA_ROOT}, name='media'),
]

