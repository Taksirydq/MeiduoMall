from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 默认拥有了用户名　密码　邮箱等属性
    # 扩展属性: 定义
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'tb_users'
