

def fail_response(msg: str = "", data=None):
    """返回失败的结果.

    :param msg: 提示信息
    :param data: 携带的数据, 单条记录用 json 对象，多条记录用 json 数组
    :return: 返回字典，flask 转化为 json 格式
    """
    return _json_response("fail", msg, data)


def success_response(msg: str = "", data=None):
    """返回成功的结果.

    :param msg: 提示信息
    :param data: 携带的数据, 单条记录用 json 对象，多条记录用 json 数组
    :return: 返回字典，flask 转化为 json 格式
    """
    return _json_response("success", msg, data)


def error_response(msg: str = "", data=None):
    """返回错误的结果.

    :param msg: 提示信息
    :param data: 携带的数据, 单条记录用 json 对象，多条记录用 json 数组
    :return: 返回字典，flask 转化为 json 格式
    """
    return _json_response("error", msg, data)


def _json_response(status: str, msg: str, data=None):
    """返回 json 格式.

    :param status: 请求状态的，fail, error, success
    :param msg: 提示的信息
    :param data: 携带的数据, 单条记录用 json 对象，多条记录用 json 数组
    :return: 返回字典，flask 转化为 json 格式
    """
    return {
        "status": status,
        "msg": msg,
        "data": data or {}
    }
