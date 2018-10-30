from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """行政区划信息序列化器"""

    class Meta:
        model = Area
        fields = ['id', 'name']


class AreaSubSerializer(serializers.ModelSerializer):
    """子行政区划信息序列化器"""
    # 关系属性, 默认以pk输出, 可以指定输出方式
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
