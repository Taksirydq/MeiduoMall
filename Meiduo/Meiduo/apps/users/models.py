from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import tjws
from . import constants
from utils.models import BaseModel


class User(AbstractUser):
    # 默认拥有了用户名　密码　邮箱等属性
    # 扩展属性: 定义
    mobile = models.CharField(max_length=11, unique=True)
    email_active = models.BooleanField(default=False)
    # 默认收货地址
    default_address = models.OneToOneField('users.Address', related_name='user_addr', null=True, blank=True)

    class Meta:
        db_table = 'tb_users'

    def generate_verify_url(self):
        # 构造有效数据
        data = {'user_id': self.id}
        # 加密
        token = tjws.dumps(data, constants.VERIFY_EMAIL_EXPIRES)
        # 构造激活链接
        return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token


class Address(BaseModel):
    # 所属用户
    user = models.ForeignKey(User, related_name='addresses')
    # 名称，例如‘家’，‘公司’
    title = models.CharField(max_length=20)
    # 收件人
    receiver = models.CharField(max_length=10)
    # 省
    province = models.ForeignKey('areas.Area', related_name='province_addr')
    # 市
    city = models.ForeignKey('areas.Area', related_name='city_addr')
    # 区县
    district = models.ForeignKey('areas.Area', related_name='district_addr')
    # 详细地址
    place = models.CharField(max_length=100)
    # 手机号
    mobile = models.CharField(max_length=11)
    # 固定电话
    tel = models.CharField(max_length=20, null=True, blank=True)
    # 邮箱
    email = models.CharField(max_length=50, null=True, blank=True)
    # 逻辑删除
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_address'
