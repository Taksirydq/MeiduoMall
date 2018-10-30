from rest_framework.response import Response
from rest_framework import generics
from .models import Area
from .serializers import AreaSerializer, AreaSubSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import CacheResponseMixin

# 方式－
# 查询多个list:返回所有的省信息
# 查询一个retrieve: 返回pk对应的地区, 并包含它的子级地区
# class AreaListView(generics.ListAPIView):
#     queryset = Area.objects.filter(parent__isnull=True)
#     serializer_class = AreaSerializer
#
#
# class AreaRetrieveView(generics.RetrieveAPIView):
#     queryset = Area.objects.all()
#     serializer_class = AreaSubSerializer


# 方式二(如果是两个视图的查询集和所指定的序列化器一样就最好使用方法二)
class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent__isnull=True)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return AreaSubSerializer
