from django.db import models
from utils.models import BaseModel
from orders.models import OrderInfo


class Payment(BaseModel):
    """
    支付信息
    """
    order = models.ForeignKey(OrderInfo, verbose_name='订单')
    trade_id = models.CharField(max_length=100, verbose_name="支付编号")

    class Meta:
        db_table = 'tb_payment'
