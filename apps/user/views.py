from django.shortcuts import render, redirect

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

from django.views import View
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord
from .forms import RegisterForm, LoginForm, ForgetPasswdForm, ResetPasswdForm
from homepage.models import RC_Article_Type, RC_Article_Tag, RC_Article, RC_Comments

import markdown
import logging

# Create your views here.

visit_logger = logging.getLogger("django")
server_logger = logging.getLogger("scripts")


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username)
            )
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveView(View):
    def get(self, request, active_code):
        records_code = EmailVerifyRecord.objects.filter(code=active_code)
        if records_code:
            for record in records_code:
                email = record.email
                user = UserProfile.objects.filter(email=email)
                if user and user[0].is_active == False:
                    user[0].is_active = True
                    user[0].save()
                    # 删除记录
                    for itm in records_code:
                        itm.delete()
                    return render(request, 'user/login.html', {})
                else:
                    msg = '用户已激活'
                    return redirect('/user/login/')
        else:
            return render(request, 'user/active_code.html', {})


class RegisterView(View):
    """注册"""

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})

    def post(self, request):
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user_name = request.POST.get('username', '')
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'user/register.html', {})
            else:
                password = request.POST.get('password', '')
                email = request.POST.get('email', '')
                userProfile = UserProfile()
                userProfile.is_active = False
                userProfile.is_active = False
                userProfile.username = user_name
                userProfile.email = email
                userProfile.password = make_password(password)
                userProfile.save()
                send_register_email(email, 'register')
                return render(request, 'user/login.html', {})
        else:
            return render(request, 'user/register.html', {})


class LoginView(View):
    """登录"""

    def get(self, request):
        return render(request, 'user/login.html', {})

    def post(self, request):
        # 验证
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user_name = request.POST.get('username', '')
            user_password = request.POST.get('password', '')
            user = CustomBackend().authenticate(request, username=user_name, password=user_password, )
            if user is not None:
                if user.is_active:
                    # 添加backend,否则会报错
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    # 测试
                    # article = RC_Article.objects.get(id=int(2))
                    # article.md_content = markdown.markdown(article.md_content, extensions=[
                    #     'markdown.extensions.extra',
                    #     'markdown.extensions.codehilite',
                    #     'markdown.extensions.toc',
                    # ])
                    # content = {'md_content': article.md_content}
                    # return render(request, 'home/index.html', content)
                    return redirect('/index/')
                else:
                    return render(request, 'user/login.html', {})
            else:
                message_error = u'用户名或是密码错误'
                return render(request, 'user/login.html', {})
        else:
            return render(request, 'user/login.html', {})


class ForgotPasswordView(View):
    """忘记密码"""

    def get(self, request):
        forget_form = ForgetPasswdForm()
        return render(request, 'user/forgot.html', {'forget_form': forget_form})

    def post(self, request):
        forget_user = ForgetPasswdForm(request.POST)
        if forget_user.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.get(email=email):
                send_register_email(email, send_type='forget', )
                return render(request, 'user/send_success.html')
            else:
                message_error = u'查无此号'
                return redirect('/user/forget/')
        else:
            message_error = u'输入错误'
            return redirect('/user/forget/')


class ResetView(View):
    """重置密码，验证验证码"""

    def get(self, request, active_code):
        # 验证码存在重复情况
        records_code = EmailVerifyRecord.objects.filter(code=active_code)
        if records_code:
            for record in records_code:
                email = record.email

                return render(request, 'user/reset_password.html', {'email': email})
        else:
            return render(request, 'user/active_code.html', {})


class ModifyPwdView(View):
    """修改密码"""

    def post(self, request):
        modify_form = ResetPasswdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                message_error = u'密码不一致'
                return render(request, 'user/reset_password.html', {'email': email, 'message': message_error})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return redirect('/user/login/')
        else:
            email = request.POST.get('email', '')
            return render(request, 'user/reset_password.html', {'email': email})
