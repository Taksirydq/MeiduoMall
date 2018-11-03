from haystack import indexes

# 如下代码可修改: 查询的模型类
from .models import SKU


# 类的名称可改, 为xxxIndex
class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    """
    # 在模板文件指定搜索的列, 可修改
    # templates/search/indexes/应用名称／模型类小写＿text.txt
    # 在模板文件中定义查询属性: {{object.属性名称}}
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型类"""
        # 模型类可以改
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        # 　查询的条件可修改
        return self.get_model().objects.filter(is_launched=True)
