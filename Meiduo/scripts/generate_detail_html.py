# !/usr/bin/env python
# 在当前环境中查找python的目录

# !/home/python/ .virtualenvs/meiduo/bin/python
# 指定当前文件执行时, 使用的解释器

# 设置环境变量
import sys
import os
import django

sys.path.insert(0, '../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Meiduo.settings.dev")
django.setup()

from goods.models import SKU
from celery_tasks.html.tasks import generate_static_sku_detail_html

if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)
    print("OK")
