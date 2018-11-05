from utils import myjson
from django_redis import get_redis_connection


def merge_cookie_to_redis(request, user_id, response):
    """
    以cookie中的商品数据为准, 如果redis中也有这个商品,则覆盖
    将cookie中的购物车信息,添加redis中,此方法供登录时调用
    :param request: 请求对象, 用于读取cookie中的购物车信息
    :param user_id: 用户编号, 用于操作redis中的购物车数据,构成键
    :param response: 响应对象,删除cookie购物车数据
    :return: 响应对象,包含了删除cookie的操作
    """
    # １.读取cookie中的购物车数据
    cart_str = request.COOKIES.get('cart')
    # 如果cookie中没有购物车信息,则直接返回
    if cart_str is None:
        return response
    # 将字符串转成字典
    cart_dict = myjson.loads(cart_str)
    # 2.遍历,写入redis中
    # 获取redis连接
    redis_cli = get_redis_connection('cart')
    # 构造键
    key_cart = 'cart_%d' % user_id
    key_selected = 'cart_selected_%d' % user_id
    # 获取管道
    redis_pipeline = redis_cli.pipeline()
    for sku_id, sku_dict in cart_dict.items():
        # hash存商品编号 数量
        redis_pipeline.hset(key_cart, sku_id, sku_dict['count'])
        # set根据选中状态存商品编号
        if sku_dict['selected']:
            redis_pipeline.sadd(key_selected, sku_id)
        else:
            redis_pipeline.srem(key_selected, sku_id)
    # 执行管道中的命令
    redis_pipeline.execute()

    # 3.删除cookie中的购物车数据
    response.set_cookie('cart', '', max_age=0)
    return response
