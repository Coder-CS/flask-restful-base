from abc import abstractmethod
from flask import Flask
from flask.views import MethodView


class ApiBase(MethodView):
    @classmethod
    @abstractmethod
    def register(cls, app: Flask):
        """ 在 Flask 中注册视图。
        """
        pass

    @classmethod
    def _register_api(cls, app: Flask, endpoint: str, url: str, pk: str = 'id', pk_type: str = 'int'):
        """ 在 Flask 创建视图函数.

            使用类试图在 Flask 中创建视图函数.

            :param app： Flask 的实例.
            :param endpoint： 用于 url_for 反向查询.
            :param url： 访问的 url 地址，不包含域名.
            :param pk： 参数名.
            :param pk_type： 参数类型.
        """
        view_func = cls.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule(f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=['GET', "PUT", 'DELETE'])
