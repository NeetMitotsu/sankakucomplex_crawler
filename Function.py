import os
import os.path
import datetime

# 图片保存位置
_folder_name = 'D:/SankakuComplex/'

def create_folder(_dic_name: str):
    global _folder_name
    if _dic_name != '': _folder_name = _dic_name
    # 创建目录存放图片
    _folder_name += datetime.datetime.now().strftime("%y%m%d")
    if not os.path.exists(_folder_name):
        os.makedirs(_folder_name)

def write(file_name: str, data, root: bool = False):
    """
    写出文件
    :param file_name: 文件名
    :param data: 数据
    :param root: 是否写到根目录
    :return:
    """
    global _folder_name
    # file_name = file_name if root else _folder_name + '/' + file_name
    file_name = os.path.join(file_name if root else os.path.join(_folder_name, file_name))
    file = open(file_name, 'wb')
    if isinstance(data, int) or isinstance(data, str):
        data = str(data).encode()
    file.write(data)
    file.close()

def get(file_name: str):
    """
    获取文件内容
    :param file_name: 文件名
    :return: str
    """
    if not os.path.exists(file_name):
        os.open(file_name, os.O_CREAT)
        return 0
    file = open(file_name)
    data = file.readline()
    file.close()
    return data

def exist(file_name: str):
    """
    文件是否存在
    :param file_name: 文件名
    :return: bool
    """
    global _folder_name
    return os.path.exists(os.path.join(_folder_name, file_name))
    # return os.path.exists(_folder_name + '/' + file_name)