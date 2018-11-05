from rest_framework.response import Response
from rest_framework.views import APIView
from goods.models import SKU
from .models import User
from .serializers import UserCreateSerializer, UserDetailSerializer \
    , EmailSerializer, EmailActiveSerializer, AddressSerializer, BrowseHistorysSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from . import constants
from rest_framework.decorators import action
from django_redis import get_redis_connection
from goods.serializers import SKUSerializer


class UsernameCountView(APIView):
    def get(self, request, username):
        # 查询用户名的个数
        count = User.objects.filter(username=username).count()
        # 响应
        return Response({
            "username": username,
            "count": count
        })


class MobileCountView(APIView):
    def get(self, request, mobile):
        # 获取指定手机号数量
        count = User.objects.filter(mobile=mobile).count()
        return Response({
            "mobile": mobile,
            "count": count
        })


class UserCreateView(CreateAPIView):
    # 创建用户
    serializer_class = UserCreateSerializer


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    # 要求必须登录(权限检查类)
    permission_classes = [IsAuthenticated]

    # 视图中封装好的代码，是根据主键查询得到的对象
    # 现在的需求: 不是根据pk查,而是要获取登录的用户
    # 解决:
    def get_object(self):
        return self.request.user


class EmailView(generics.UpdateAPIView):
    """发送邮件实现"""
    # 要求登录, 则request.user才有意义
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    # 修改当前登录用户的email属性
    def get_object(self):
        return self.request.user


class EmailActiveView(APIView):
    """验证邮箱链接接口实现"""

    def get(self, request):
        # 接收数据并验证
        serializer = EmailActiveSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors)

        # 查询当前用户, 并修改属性
        user = User.objects.get(pk=serializer.validated_data.get('user_id'))
        user.email_active = True
        user.save()
        # 响应
        return Response({'message': 'OK'})


class AddressViewSet(ModelViewSet):
    """用户地址管理"""
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    # 指定查询集
    def get_queryset(self):
        return self.request.user.addresses.filter(is_delete=False)

    # list----->查询多个[{], {]]
    # 重写
    def list(self, request, *args, **kwargs):
        # 查询数据
        address_list = self.get_queryset()
        # 创建序列化器对象
        serializer = self.get_serializer(address_list, many=True)
        # 返回值的结构
        """
        {
            "user_id" : 用户编号，
            "default_address_id": 默认收货地址编号，
            "limit": 每个用户的收货地址数量上限，
            "addresses": 地址数据, 格式如[{地址的字典}，{},......]
        
        }
        
        """
        return Response({
            "user_id": self.request.user.id,
            "default_address_id": self.request.user.default_address_id,
            "limit": constants.ADDRESS_LIMIT,
            "addresses": serializer.data
        })

    # destroy-->物理删除,　重写,　实现逻辑删除
    def destroy(self, request, *args, **kwargs):
        """实现地址逻辑删除"""
        # 根据主键查询对象
        address = self.get_object()
        # 逻辑删除
        address.is_delete = True
        # 保存
        address.save()
        # 响应
        return Response(status=204)

    # 修改标题--->/pk/title/------>put
    # 如果没有detail=False---->* * */title/
    @action(methods=['put'], detail=True)
    def title(self, request, pk):
        """修改标题"""
        # 根据主键查询收货地址
        address = self.get_object()
        # 接收数据, 修改标题属性
        address.title = request.data.get('title')
        # 保存
        address.save()
        # 响应
        return Response({'title': address.title})

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        """设置默认收货地址"""
        # 查找当前登录用户
        user = request.user
        # 修改属性
        user.default_address_id = pk
        # 保存
        user.save()
        # 响应
        return Response({'message': 'OK'})


class BrowseHistoryView(generics.ListCreateAPIView):
    """用户浏览历史记录"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # 创建与查询列表使用不同的序列化器
        if self.request.method == 'GET':
            return SKUSerializer
        else:
            return BrowseHistorysSerializer

    # 查询需要指定查询集
    def get_queryset(self):
        # 连接redis
        redis_cli = get_redis_connection('history')
        # 查询当前登录用户的浏览记录[sku_id, sku_id, ....]
        key = 'history_%d' % self.request.user.id
        sku_ids = redis_cli.lrange(key, 0, -1)
        # 遍历列表, 根据sku_id查询商品对象
        skus = []
        for sku_id in sku_ids:
            skus.append(SKU.objects.get(pk=int(sku_id)))
        return skus  # [sku对象, sku对象, sku对象 .....]
