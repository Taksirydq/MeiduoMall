from rest_framework import serializers
from .models import SKU
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import SKUIndex


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'default_image_url', 'comments']


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    # 指定数据的序列化器
    object = SKUSerializer(read_only=True)

    class Meta:
        # 索引类的名称可改
        index_classes = [SKUIndex]
        fields = (
            'text',  # 用于接收查询关键字
            'object'  # 用于返回查询结果
        )
