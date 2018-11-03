from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Meiduo.settings.dev'

# 创建celery对象
app = Celery('meiduo')

# 加载配置
app.config_from_object('celery_tasks.config')

# 自动识别任务
app.autodiscover_tasks([
    'celery_tasks.sms',
    'celery_tasks.email',
    'celery_tasks.html'
])


