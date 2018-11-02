from rest_framework.generics import ListAPIView
from .models import SKU
from rest_framework.filters import OrderingFilter
from utils.pagination import SKUListPagination
from .serializers import SKUSerializer


class SKUListView(ListAPIView):
    def get_queryset(self):
        # 查询多个时, 获取路径中的参数: self.kwargs---->字典
        return SKU.objects.filter(category_id=self.kwargs['category_id'])

    serializer_class = SKUSerializer

    # 分页
    pagination_class = SKUListPagination

    # 排序
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_time', 'price', 'sales']
