from flask.views import MethodView
from flask import Flask


class ApiBase(MethodView):
    @classmethod
    def register(cls, app: Flask, endpoint: str, url: str, pk: str = 'id', pk_type: str = 'int'):
        view_func = cls.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule(f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=['GET', "PUT", 'DELETE'])