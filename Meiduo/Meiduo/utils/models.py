from django.db import models


class BaseModel(models.Model):
    # 创建时间，创建对象时，默认设置成当前时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间, 修改对象时，默认设置成当前时间
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        # 当前模型类并不需要生成一张表,用于其它模型类的继承
        abstract = True
