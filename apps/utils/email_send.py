from django.core.mail import send_mail
from django.conf import settings

from user.models import EmailVerifyRecord
import random


def random_str(random_length=8):
    code_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars) - 1
    for i in range(random_length):
        code_str += chars[random.randint(0, length)]
    return code_str


def send_register_email(email: str, send_type='register', ):
    email_record = EmailVerifyRecord()
    code = random_str(random_length=16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    to_email = email

    if send_type == 'register':
        email_title = u'博客注册激活'
        email_content = u'请点击下方链接进行激活：http:127.0.0.1:8000/user/active/{0}'.format(code)
        send_mail(email_title, email_content, settings.DEFAULT_FROM_EMAIL, [email])

    if send_type == 'forget':
        email_title = u'博客密码重置'
        email_content = u'请点击下方链接进行重置：http:127.0.0.1:8000/user/reset/{0}'.format(code)
        send_mail(email_title, email_content, settings.DEFAULT_FROM_EMAIL, [email])
