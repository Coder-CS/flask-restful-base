from abc import abstractmethod
from flask import Flask, jsonify
from flask.views import MethodView

from app.token import Token, TokenState
from app import redis_db


class ApiBase(MethodView):
    @classmethod
    @abstractmethod
    def register(cls, app: Flask):
        """ 在 Flask 中注册视图。
        """
        pass

    @staticmethod
    def ok_json(msg: str = "", data: dict = None):
        if data is None:
            data = {}
        return ApiBase.json_response("ok", msg, data)

    @staticmethod
    def err_json(msg: str = "", data: dict = None):
        if data is None:
            data = {}
        return ApiBase.json_response("err", msg, data)

    @staticmethod
    def json_response(state: str, msg: str, data: dict):
        return jsonify({
            "state": state,
            "msg": msg,
            "data": data
        })

    @staticmethod
    def get_redis_key(id):
        return f"user_token_{id}"

    @staticmethod
    def work_with_token(token: str, secret_key: str, func):
        state, data = Token.verify_token(token, secret_key)
        if state == TokenState.Valid:
            if not data.has_key("id"):
                return ApiBase.err_json("无效的令牌")
            key = ApiBase.get_redis_key(data["id"])
            test_token = redis_db.get(key)
            if test_token and test_token != token:
                return ApiBase.err_json("无效的令牌")
            return func(data)
        elif state == TokenState.Expired:
            return ApiBase.err_json("令牌已过期")
        else:
            return ApiBase.err_json("无效的令牌")

    @classmethod
    def _register_api(cls, app: Flask, endpoint: str, url: str, pk: str = 'id', pk_type: str = 'int'):
        """在 Flask 中注册视图

        :param app: Flask 的实例.
        :param endpoint: 用于 url_for 反向查询.
        :param url: 访问的 url 地址，不包含域名.
        :param pk: 参数名.
        :param pk_type: 参数类型.
        :return: None
        """
        view_func = cls.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule(f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=['GET', "PUT", 'DELETE'])
