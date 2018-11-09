from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from goods.models import SKU
from utils import myjson
from . import constants
from django_redis import get_redis_connection


class CartView(APIView):
    # 在执行视图函数前, 不进行身份检查,重写用户认证方法
    def perform_authentication(self, request):
        pass

    def post(self, request):
        # 判断用户是否登录
        try:
            # 如果用户认证信息不存在则抛异常
            user = request.user
        except:
            user = None
        # 接收请求数据, 进行验证
        serializer = serializers.CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 验证通过后获取数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']

        # 构造响应对象
        response = Response(serializer.validated_data)

        if user is None:
            """Cookie"""
            # 如果未登录, 则存入cookie
            # 读取cookie中的数据
            cart_str = request.COOKIES.get('cart')
            if cart_str is None:
                cart_dict = {}
            else:
                cart_dict = myjson.loads(cart_str)
            # 取出原数量
            if sku_id in cart_dict:
                count_cart = cart_dict[sku_id]['count']
            else:
                count_cart = 0
            # 修改数据
            cart_dict[sku_id] = {
                'count': count + count_cart,
                'selected': True
            }
            # 写cookie
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            """Redis"""
            # 如果已登录, 则存入redis
            # 连接redis
            redis_cli = get_redis_connection('cart')
            # 构造键, 因为服务器会存多个用户的购物车信息, 通过用户编号可以区分
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            # 将商品编号 数量存入hash中
            redis_cli.hset(key, sku_id, count)
            # 将商品编号存入set中,表示选中此是商品
            redis_cli.sadd(key_select, sku_id)
        return response

    def get(self, request):
        try:
            user = request.user
        except:
            user = None
        if user is None:
            # 未登录, 读取cookie
            # 获取cookie中购物车信息
            cart_str = request.COOKIES.get('cart')
            if cart_str is None:
                return Response()
            cart_dict = myjson.loads(cart_str)
            # 根据商品编号查询对象,并添加数量 选中属性
            skus = []
            for key, value in cart_dict.items():
                sku = SKU.objects.get(pk=key)
                # 给商品增加属性
                sku.count = value['count']
                sku.selected = value['selected']
                skus.append(sku)
        else:
            # 已登录, 读redis
            # 连接redis
            redis_cli = get_redis_connection('cart')
            # 构造键, 因为服务器会存多个用户的购物车信息,通过用户编号可以区分
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            # 从hash中读取所有商品编号
            sku_ids = redis_cli.hkeys(key)
            # 读取选中的商品编号
            sku_ids_selected = redis_cli.smembers(key_select)
            sku_ids_selected = [int(sku_id) for sku_id in sku_ids_selected]
            # 查询商品
            skus = SKU.objects.filter(pk__in=sku_ids)
            # 遍历商品 增加数量 选中属性
            for sku in skus:
                sku.count = redis_cli.hget(key, sku.id)
                sku.selected = sku.id in sku_ids_selected
        # 序列化输出
        serializer = serializers.CartSerializer(skus, many=True)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = request.user
        except:
            user = None
        # 接收数据并验证
        serializer = serializers.CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 验证通过后获取数据
        count = serializer.validated_data['count']
        sku_id = serializer.validated_data['sku_id']
        selected = serializer.validated_data['selected']

        response = Response(serializer.validated_data)

        if user is None:
            # 未登录,操作cookie
            # 1.读取
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            # 2.修改
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 3.保存
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            # 已登录, 操作redis
            # 连接redis
            redis_cli = get_redis_connection('cart')
            # 构造键, 因为服务器会存入多个用户的购物车信息, 通过用户编号可以区分
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            # 修改数量
            redis_cli.hset(key, sku_id, count)
            # 修改选中
            if selected:
                redis_cli.sadd(key_select, sku_id)
            else:
                redis_cli.srem(key_select, sku_id)
        return response

    def delete(self, request):
        try:
            user = request.user
        except:
            user = None
        serializer = serializers.CartDeleteSerializer(data=request.data)  # 返回解析之后请求体的数据
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.validated_data['sku_id']
        response = Response(status=204)
        if user is None:
            # 读取cookie
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            # 删除
            if sku_id in cart_dict:
                del cart_dict[sku_id]
            # 保存到cookie中
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            # 连接redis
            redis_cli = get_redis_connection('cart')
            # 构造键, 因为服务器会存入多个用户购物车信息, 通过用户编号可以区分
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            # hash
            redis_cli.hdel(key, sku_id)
            # set
            redis_cli.srem(key_select, sku_id)
        return response


class CartSelectView(APIView):
    def perform_authentication(self, request):
        pass

    def put(self, request):
        try:
            user = request.user
        except:
            user = None
        serializer = serializers.CartSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected = serializer.validated_data['selected']
        response = Response({'message': 'OK'})
        if user is None:
            """Cookie"""
            cart_str = request.COOKIES.get('cart')
            cart_dict = myjson.loads(cart_str)
            for key in cart_dict.keys():
                cart_dict[key]['selected'] = selected
            cart_str = myjson.dumps(cart_dict)
            response.set_cookie('cart', cart_str, max_age=constants.CART_COOKIE_EXPIRES)
        else:
            """Redis版"""
            # 连接redis
            redis_cli = get_redis_connection('cart')
            # 构造键, 因为服务器会存入多个用户信息的购物车信息, 通过用户编号可以区分
            key = 'cart_%d' % request.user.id
            key_select = 'cart_selected_%d' % request.user.id
            # 获取所有商品编号, hash
            sku_ids = redis_cli.hkeys(key)
            # 选中
            if selected:
                redis_cli.sadd(key_select, *sku_ids)
            else:
                redis_cli.srem(key_select, *sku_ids)
        return response
