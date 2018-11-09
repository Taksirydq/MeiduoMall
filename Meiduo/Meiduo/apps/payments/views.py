from rest_framework.views import APIView
from orders.models import OrderInfo
from alipay import AliPay
from django.conf import settings
from rest_framework.response import Response
from .models import Payment


class AliPayURLView(APIView):
    def get(self, request, order_id):
        # 1.根据order_id查询订单对象
        try:
            order = OrderInfo.objects.get(pk=order_id)
        except:
            raise Exception('订单编号无效')

        # 2.创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=settings.ALIPAY_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG
        )
        # 3.调用方法生成url
        order_string = alipay.api_alipay_trade_page_pay(
            subject=settings.ALIPAY_SUBJECT,
            out_trade_no=order_id,  # 订单编号
            total_amount=str(order.total_amount),  # 支付总金额,　类型为Decimal(),不支持序列化，需要强转成str
            return_url=settings.ALIPAY_RETURN_URL  # 支付成功后的回调地址
        )
        # 4. 返回url
        return Response({'alipay_url': settings.ALIPAY_GATE + order_string})


class OrderStatusView(APIView):
    def put(self, request):
        # 1.接收支付宝返回的数据
        alipay_dict = request.query_params.dict()

        # 2.验证是否支付成功
        # 2.1删除签名,不参与验证
        signature = alipay_dict.pop('sign')
        # 2.2创建alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=settings.ALIPAY_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG
        )
        # 2.2调用verify(字典，签名)
        success = alipay.verify(alipay_dict, signature)
        if success:
            # 支付成功
            """
            'charset':'utf-8 '　编码
            'out_trade_no': '20181107205456000000002' 　商城的订单编号
            'method': 'alipay.trade.page.pay.return'
            'total_amount': '3788.00', 　支付金额
            'trade_no': '2018110722001460600500458823' 流水号
            'auth_app_id': '2016092000553146' 应用编号
            'version': '1.0' 版本
            """
            # print(alipay_dict) # 一个字典　　如上
            order_id = alipay_dict['out_trade_no']
            # 2.2.1修改订单状态
            try:
                order = OrderInfo.objects.get(pk=order_id)
            except:
                raise Exception('订单编号无效')
            else:
                order.status = 2  # 更改订单状态
                order.save()
            # 2.2.2创建订单支付对象
            trade_no = alipay_dict.get('trade_no')
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_no
            )

            # 响应
            return Response({'trade_id': trade_no})
        else:
            raise Exception('支付失败')
