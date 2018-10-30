from rest_framework.views import APIView
from rest_framework.response import Response
from .qq_sdk import OAuthQQ
from .models import QQUser
from utils import tjws
from . import constants
from utils.jwt_token import generate
from .serializers import QQBindSerializer


class QQurlView(APIView):
    """返回QQ登录页面"""

    def get(self, request):
        # 接收登录后的地址
        # next: 表示用户登录成功后访问那个网址
        state = request.query_params.get('next')
        # 创建工具类对象
        oauthqq = OAuthQQ(state=state)
        # 获取授权地址
        url = oauthqq.get_qq_login_url()
        # 响应
        return Response({
            'login_url': url
        })


class QQLoginView(APIView):
    """QQ登录成功后的回调处理"""

    def get(self, request):
        # 获取code
        # query_params：获取查询字符串的数据
        code = request.query_params.get('code')
        # 根据code获取token
        oauthqq = OAuthQQ()
        token = oauthqq.get_access_token(code)
        # 根据token获取openid
        openid = oauthqq.get_openid(token)
        # 查询openid是否存在
        try:
            qquser = QQUser.objects.get(openid=openid)
        except:
            # 如果不存在，则通知客户端转到绑定页面
            # 将openid加密进行输出
            data = tjws.dumps({'openid': openid}, constants.BIND_TOKEN_EXPIRES)
            # 响应
            return Response({
                'access_token': data
            })
        else:
            # 如果存在，则状态保持，表示登录成功
            return Response({
                'user_id': qquser.user.id,
                'username': qquser.user.username,
                'token': generate(qquser.user)
            })

    def post(self, request):
        """登录成功后的绑定视图"""
        # 接收(获取到请求体里数据赋给data，创建一个序列化器对象)
        serializer = QQBindSerializer(data=request.data)
        # 验证
        if not serializer.is_valid():
            return Response({'message': serializer.errors})
        # 绑定: 在qquser表中创建一条数据
        qquser = serializer.save()
        # 响应: 绑定完成,表示登录成功,状态保存
        return Response({
            'user_id': qquser.user.id,
            'username': qquser.user.username,
            'token': generate(qquser.user)

        })
