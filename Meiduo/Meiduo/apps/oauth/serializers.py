from rest_framework import serializers
from .models import QQUser
from users.models import User
from utils import tjws
from . import constants
import re
from django_redis import get_redis_connection


class QQBindSerializer(serializers.Serializer):
    # 定义属性
    mobile = serializers.CharField()
    password = serializers.CharField()
    sms_code = serializers.CharField()
    access_token = serializers.CharField()

    # 验证
    def validate(self, attrs):
        # 短信验证码是否正确
        # 1.获取请求报文中的短信验证码　手机号
        sms_code_request = attrs.get('sms_code')
        mobile = attrs.get('mobile')
        # 2.获取redis中的短信验证码
        redis_cli = get_redis_connection('sms_code')
        sms_code_redis = redis_cli.get('sms_code_' + mobile)
        # 3.判断是否过期
        if sms_code_redis is None:
            raise serializers.ValidationError('短信验证码已过期')
        # 4.强制立即过期
        redis_cli.delete('sms_code_' + mobile)
        # 5.判断获取的两个验证码是否相等
        if int(sms_code_request) != int(sms_code_redis):
            raise serializers.ValidationError('短信验证码错误')

        # 验证:access_token
        # 1.解密
        data_dict = tjws.loads(attrs.get('access_token'), constants.BIND_TOKEN_EXPIRES)
        # 2.判断是否过期
        if data_dict is None:
            raise serializers.ValidationError('access_token已过期')
        # 获取openid
        openid = data_dict.get('openid')
        # 加入字典
        attrs['openid'] = openid

        return attrs

    # 保存：创建
    def create(self, validated_data):
        # validated_data表示验证后的数据
        mobile = validated_data.get('mobile')
        openid = validated_data.get('openid')
        password = validated_data.get('password')
        # 1.查询手机号是否对应着一个用户
        try:
            user = User.objects.get(mobile=mobile)
        except:
            # 3.如果没有对应着一个用户
            # 3.1创建用户
            user = User()
            user.username = mobile
            user.mobile = mobile
            user.set_password(password)
            user.save()
        else:
            # 2.如果对应着一个用户，进行密码对比
            # 2.1如果密码错误则抛异常
            if not user.check_password(password):
                raise serializers.ValidationError('此手机号已经被使用')
        # 绑定：创建QQUser对象
        qquser = QQUser()
        qquser.openid = openid
        qquser.user = user
        qquser.save()

        return qquser
