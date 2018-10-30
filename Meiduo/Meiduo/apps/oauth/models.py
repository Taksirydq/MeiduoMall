from django.db import models
from utils.models import BaseModel


class QQUser(BaseModel):
    # openid就是QQ账号在QQ网站的唯一标识
    openid = models.CharField(max_length=64)
    # 关联本网站的用户
    user = models.ForeignKey('users.User')

    class Meta:
        """QQ授权登录表"""
        db_table = 'tb_oauth_qq'
