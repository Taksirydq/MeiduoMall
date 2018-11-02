import os
from django.conf import settings
from .models import ContentCategory
from django.shortcuts import render
from utils.goods_category import get_goods_category


def generate_index_html():
    # 1.1 查询分类数据
    categories = get_goods_category()

    # 1.2 查询广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for category in content_categories:
        # 广告的位置对应的一个广告的数据
        contents[category.key] = category.content_set.filter(status=True).order_by('sequence')

    # 2.生成html标签, 写到html文件中
    # 2.1 生成html字符串
    response = render(None, 'index.html', {'categories': categories, 'contents': contents})
    html_str = response.content.decode()
    # 2.2 写文件
    filename = os.path.join(settings.GENERATE_STATIC_HTML_PATH, 'index.html')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_str)
    print('OK')

