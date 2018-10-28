from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings


def dumps(data, expires):
    # 创建对象
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires)
    # 加密
    result = serializer.dumps(data).decode()
    return result


def loads(data, expires):
    # 创建对象
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires)
    # 解密
    try:
        data_dict = serializer.loads(data)
        return data_dict
    except:
        # 抛异常的原因:超时
        return None