_log_msg = ''


def add(msg: str):
    """
    添加日志信息
    :param msg:
    :return:
    """
    global _log_msg
    _log_msg += msg + '\r\n'
    print(msg)

def get():
    """
    获取日志内容
    :return:
    """
    global _log_msg
    return _log_msg
