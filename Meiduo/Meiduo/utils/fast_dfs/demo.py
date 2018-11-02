from fdfs_client.client import Fdfs_client

if __name__ == '__main__':
    client = Fdfs_client('client.conf')
    ret = client.upload_by_file('/home/python/Desktop/1.jpg')
    print(ret)
    '''
    {
    'Uploaded size': '12.00KB',
    'Status': 'Upload successed.',
    'Storage IP': '192.168.247.128',
    'Group name': 'group1',
    'Local file name': '/home/python/Desktop/pic/avatar/1.jpg',
    'Remote file_id': 'group1/M00/00/02/wKj3gFvaou-ACZ2EAAAwL_xHUtE202.jpg'
    }
    '''
