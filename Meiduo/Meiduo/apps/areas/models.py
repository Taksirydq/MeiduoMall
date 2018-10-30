from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=20)
    # ForeignKey('self'): 代表自关联的字段的外键指向自身
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subs')

    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
