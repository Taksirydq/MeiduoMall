from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import serializers
import random
from utils.ytx_sdk.sendSMS import CCP
from . import constants
from celery_tasks.sms.tasks import send_sms_code


class SMSCodeView(APIView):
    # 发送短信验证码接口
    def get(self, request, mobile):
        """
        限制60秒内只能向个一个手机号码发送一次短信验证码

        """
        # 获取Redis的连接: 从配置中的cache处，根据名称获取连接
        redis_cli = get_redis_connection('sms_code')
        # 1.判断60秒内是不是向指定手机号码发过短信，如果发过,则抛异常
        if redis_cli.get('sms_flag_' + mobile):
            raise serializers.ValidationError('您发送短信太过频繁')
        # 2.如果未发短信,则随机生成6位随机数
        code = random.randint(100000, 999999)
        # 2.1 保存到redis:验证码,发送的标记　优化(使用pipeline管道)
        redis_pipeline = redis_cli.pipeline()
        redis_pipeline.setex('sms_code_' + mobile, constants.SMS_CODE_EXPIRES, code)
        redis_pipeline.setex('sms_flag_' + mobile, constants.SMS_FLAG_EXPIRES, 1)
        redis_pipeline.execute()
        # 3.发送短信:云通讯
        # CCP.sendTemplateSMS(mobile, code, constants.SMS_CODE_EXPIRES/60, 1)
        #  调用celery任务,执行耗时代码
        send_sms_code.delay(mobile, code, constants.SMS_CODE_EXPIRES/60, 1)
        # 4.响应
        return Response({'message': 'ok'})
