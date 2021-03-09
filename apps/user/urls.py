from django.urls import path, re_path
from .views import LoginView, RegisterView, ActiveView, ForgotPasswordView, ResetView, ModifyPwdView


urlpatterns = [
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'register/', RegisterView.as_view(), name='register'),
    re_path(r'active/(?P<active_code>.*)', ActiveView.as_view(), name='user_active'),
    path(r'forget/', ForgotPasswordView.as_view(), name='forget_password'),
    re_path(r'reset/(?P<active_code>.*)', ResetView.as_view(), name='reset_password'),
    path(r'modifypwd/', ModifyPwdView.as_view(), name='modify_pwd'),
]