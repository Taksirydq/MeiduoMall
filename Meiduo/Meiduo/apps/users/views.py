from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserCreateSerializer, UserDetailSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
    # 要求登录
    permission_classes = [IsAuthenticated]

    # 视图中封装好的代码，是根据主键查询得到的对象
    # 现在的需求: 不是根据pk查,而是要获取登录的用户
    # 解决:
    def get_object(self):
        return self.request.user
