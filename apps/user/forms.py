from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPasswdForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetPasswdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, )
    password2 = forms.CharField(required=True, min_length=6, )
    email = forms.EmailField(required=True)
