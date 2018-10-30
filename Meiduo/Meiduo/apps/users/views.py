from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserCreateSerializer, UserDetailSerializer \
    , EmailSerializer, EmailActiveSerializer, AddressSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from . import constants


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
