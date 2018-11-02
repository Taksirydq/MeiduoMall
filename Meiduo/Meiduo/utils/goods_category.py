from collections import OrderedDict
from goods.models import GoodsChannel


def get_goods_category():
    # 1.查询分类数据 广告数据
    # 1.1 查询分类数据
    """
    {
    组编号（同频道）:{
            一级分类channels：[]-->键
            二级分类sub_cats：[]
        }
    }
    如：
    {
        1:{
            channels:[
                {手机},{相机},{数码}
            ],
            sub_cats:[二级分类]
        },
        2:{
            channels:[
                {电脑},{办公},{家用电器}
            ],
            sub_cats:[二级分类]
        },
        ....
    }
    """
    # OrderedDict(): 一个有序的字典
    categories = OrderedDict()
    # 查到所有的频道先按组排序, 如果组排序一样的就按组内的顺序进行排序
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        # channel.group_id===>组编号
        # channel.category====>一级分类
        # channel.url=========>一级分类的链接
        # 判断这个组在最大的这个字典里有没有
        if channel.group_id not in categories:
            # 如果没有就新增一个组，然后给他加上一个一级分类列表和二级分类列表
            categories[channel.group_id] = {'channels': [], 'sub_cats': []}
            # 添加一级分类　channel.group_id: 某个组的编号
            # categories: 一个频道字典
        categories[channel.group_id]['channels'].append({
            'id': channel.id,  # 频道id
            'name': channel.category.name,  # 频道名称
            'url': channel.url  # 每个一级分类都有个自己的链接
        })
        # 添加二级分类
        sub_cats = channel.category.goodscategory_set.all()
        # 添加三级分类
        for sub in sub_cats:
            sub.sub_cats = sub.goodscategory_set.all()
            categories[channel.group_id]['sub_cats'].append(sub)

    return categories