from django.contrib.auth.backends import ModelBackend
from .models import User
import re


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class MyModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 判断username是用户名,还是手机号
            if re.match(r'^1[3-9]\d{9}$', username):
                # 手机号
                user = User.objects.get(mobile=username)
            else:
                # 用户名
                user = User.objects.get(username=username)
        except:
            # 没有查询到就返回空
            return None

        # 判断密码
        if user.check_password(password):
            # 返回user对象
            return user
        else:
            return None
