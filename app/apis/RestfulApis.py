from flask import Flask
from flask.views import MethodView

from app.apis.ApiBase import ApiBase


class UserApi(ApiBase):
    @classmethod
    def register(cls, app: Flask):
        cls._register_api(app, "users", "/users/", "id", "int")

    def get(self, id):
        print(id)
        if id is None:
            return "users"
        else:
            return "user"

    def post(self, id):
        return str(id)
