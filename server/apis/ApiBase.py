from abc import abstractmethod
from flask import Flask, jsonify
from flask.views import MethodView

from server.token import Token, TokenState
from server import redis_db
from server.response import error_response, success_response, fail_response


class ApiBase(MethodView):
    @classmethod
    @abstractmethod
    def register_api(cls, app: Flask):
        """ 在 Flask 中注册视图。
        """
        pass

    @staticmethod
    def get_redis_key(prefix: str, id):
        return f"{prefix}_{id}"

    @staticmethod
    def check_json(json, *args) -> (bool, str):
        """验证 json 信息

        :param json: 要验证的 json
        :param args: 要验证的所有 key
        :return: 返回 bool，提示信息
        """
        if json is None or not isinstance(json, dict):
            return False, "没有有效数据"
        for arg in args:
            test = json.get(arg)
            if test is None or len(test.strip()) == 0:
                return False, f"{arg} 不能为空"
        return True, "验证通过"

    @staticmethod
    def check_token(token: str, secret_key: str, redis_key_prefix: str):
        """验证token

        :param redis_key_prefix: 存储在 redis 中的 key 的前缀，如 login_token, 则 key 为 login_token_1
        :param token: 令牌
        :param secret_key: 密钥
        :return: 返回 { "status": status, "msg": msg, "data": data or {} }
        """
        if token is None:
            return error_response("Token 为空")
        state, data = Token.verify_token(token, secret_key)
        if state == TokenState.Valid:
            if "id" not in data:
                return error_response("无效的令牌")
            key = ApiBase.get_redis_key(redis_key_prefix, data.get("id"))
            test_token = redis_db.get(key)
            if test_token and test_token != token:
                return error_response("无效的令牌")
            return success_response("验证成功", data)
        elif state == TokenState.Expired:
            return error_response("令牌已过期")
        else:
            return error_response("无效的令牌")

    @classmethod
    def _register_api(cls, app: Flask, endpoint: str, url: str, pk: str = 'id',
                      pk_type: str = 'string', url_prefix: str = "/api"):
        """在 Flask 中注册视图

        :param app: Flask 的实例.
        :param endpoint: 用于 url_for 反向查询.
        :param url: 访问的 url 地址，不包含域名.
        :param pk: 参数名.
        :param pk_type: 参数类型.
        :param url_prefix: url 前缀
        :return: None
        """
        combine_url = f"{url_prefix}{url}"
        view_func = cls.as_view(endpoint)
        app.add_url_rule(combine_url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
        app.add_url_rule(combine_url, view_func=view_func, methods=['POST', ])
        app.add_url_rule(f"{combine_url}/<{pk_type}:{pk}>", view_func=view_func, methods=['GET', "PUT", 'DELETE'])
