from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client


@deconstructible()
class Fast_DFSStorage(Storage):
    def open(self, name, mode='rb'):
        # 文件保存在fastdfs中, 读取由fastdfs做, 不需要django操作, 此方法无用
        pass

    def save(self, name, content, max_length=None):
        # content: 请求报文中的文件对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 读取文件的字节数据
        ret = client.upload_by_buffer(content.read())
        if ret['Status'] != 'Upload successed.':
            raise Exception('文件保存失败')
        return ret['Remote file_id']

    def exists(self, name):
        """
        判断文件是否存在,FastDFS可以自行解决文件的重命名问题
        所以此处返回False,告诉django上传的都是新文件
        """
        return False

    def url(self, name):
        """返回文件的完整的URL路径"""
        print(settings.FDFS_URL + name)
        return settings.FDFS_URL + name
