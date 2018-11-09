import xadmin
from xadmin import views
from . import models


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "美多商城运营管理系统"  # 设置站点标题
    site_footer = "美多商城集团有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):
    model_icon = 'fa fa-gift'
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    search_fields = ['id', 'name']
    list_filter = ['is_launched']
    list_editable = ['price', 'stock']
    show_detail_fields = ['name']
    show_bookmarks = True
    list_export = ['xls', 'csv', 'xml']
    refresh_times = [3, 5]
    data_charts = {
        "sku_stock": {
            'title': '库存量',
            "x-field": "id",
            "y-field": ('stock',),
            "order": ('id',)
        },
        "sku_sales": {
            'title': '销量',
            "x-field": "id",
            "y-field": ('sales',),
            "order": ('id',)
        },
    }
    readonly_fields = ['sales', 'comments']

    def save_models(self):
        # 当对象被添加时　修改时执行
        obj = self.new_obj
        obj.save()

    def delete_model(self):
        # 当对象被删除时执行
        obj = self.obj
        obj.delete()


xadmin.site.register(models.GoodsCategory)
xadmin.site.register(models.GoodsChannel)
xadmin.site.register(models.Goods)
xadmin.site.register(models.Brand)
xadmin.site.register(models.GoodsSpecification)
xadmin.site.register(models.SpecificationOption)
xadmin.site.register(models.SKU, SKUAdmin)
xadmin.site.register(models.SKUSpecification)
xadmin.site.register(models.SKUImage)
