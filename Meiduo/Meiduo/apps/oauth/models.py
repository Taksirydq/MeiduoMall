from django.db import models
from utils.models import BaseModel


class QQUser(BaseModel):
    # QQ账号在QQ网站的唯一标识
    openid = models.CharField(max_length=64)
    # 关联本网站的用户
    user = models.ForeignKey('users.User')

    class Meta:
        db_table = 'tb_oauth_qq'
