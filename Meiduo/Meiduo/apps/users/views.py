from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserCreateSerializer
from rest_framework.generics import CreateAPIView


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
