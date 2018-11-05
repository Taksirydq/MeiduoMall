from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from goods.models import SKU
from carts.serializers import CartSerializer
from rest_framework.generics import CreateAPIView
from .serializers import OrderCreateSerializer

class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1.读取redis中的购物车数据
        redis_cli = get_redis_connection('cart')
        key_cart = 'cart_%d' % request.user.id
        key_selected = 'cart_selected_%d' % request.user.id
        # hash--->读取商品编号, 表示选中的商品
        cart_dict = redis_cli.hgetall(key_cart)  # {sku_id:count,....}
        # set----->读取商品编号,表示选中的商品
        cart_selected = redis_cli.smembers(key_selected)  # [sku_id, ...]
        # 将redis中读取的字节转换成int
        cart_dict2 = {}
        for sku_id, count in cart_dict.items():
            cart_dict2[int(sku_id)] = int(count)
        cart_selected2 = [int(sku_id) for sku_id in cart_selected]

        # 查询商品对象
        skus = SKU.objects.filter(pk__in=cart_selected2)
        # 遍历,增加数量属性
        for sku in skus:
            sku.count = cart_dict2[sku.id]
            sku.selected = True

        # 3.序列化输出
        serializer = CartSerializer(skus, many=True)
        return Response({
            'freight': 10,
            'skus': serializer.data
        })


class OrderCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer