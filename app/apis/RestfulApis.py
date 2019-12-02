from flask import Flask
from flask import request
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from app.apis.ApiBase import ApiBase
from app.models import User
from app.token import TokenState, Token
from app.config import setting
from app import redis_db, db
from app.email import is_valid_email

SECRET_KEY = setting.get("SECRET_KEY")
SECONDS = 259200  # 3 天


class UserApi(ApiBase):
    @classmethod
    def register(cls, app: Flask):
        cls._register_api(app, "users", "/users/", "token", "string")

    def get_user(self, token_data: dict):
        user = User.query.filter_by(id=token_data.id).first()
        return self.ok_json("验证通过", {"name": user.name})

    def generate_new_token(self, token_data: dict):
        id = token_data.get("id")
        token = Token.generate_token(SECRET_KEY, SECONDS, **token_data)
        key = self.get_redis_key(id)
        redis_db.set(key, token, SECONDS)
        return self.ok_json("验证成功", {"token": token})

    def post_func(self, data, func):
        password = data.get("password", "").strip()
        email = data.get("email", "").strip()
        if not len(password) > 0:
            return self.err_json("密码无效")
        if not is_valid_email(email):
            return self.err_json("Email 无效")
        return func(data, email, password)

    def register_user(self, data, email, password):
        name = data.get("name", "").strip()
        if "name" not in data or not len(name) > 0:
            return self.err_json("姓名无效")
        else:
            User.add_user(email, name, password)
            return self.ok_json("注册成功")

    def login(self, data, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            token = Token.generate_token(SECRET_KEY, SECONDS, id=user.id)
            key = self.get_redis_key(user.id)
            redis_db.set(key, token, SECONDS)
            return self.ok_json("登录成功", {"token": token})
        else:
            return self.err_json("用户名或密码错误")

    def get(self, token):
        if token is None:
            return self.err_json(msg="无效的请求")
        else:
            return self.work_with_token(token, SECRET_KEY, self.get_user)

    def post(self):
        data = request.json
        if not data:
            return self.err_json("数据无效")
        action = data.get("action", "").strip()
        if action == "register":
            return self.post_func(self.register_user)
        elif action == "login":
            return self.post_func(self.login)
        else:
            return self.err_json("无效的操作")

    def put(self, token):
        return self.work_with_token(token, SECRET_KEY, self.generate_new_token)

    def delete(self, token):
        pass
