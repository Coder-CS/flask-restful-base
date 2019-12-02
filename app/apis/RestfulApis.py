from enum import Enum
from flask import Flask
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.apis.ApiBase import ApiBase


class TokenState(Enum):
    Expired = 1
    Invalid = 2
    Valid = 3


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


class AuthApi(ApiBase):
    @staticmethod
    def generate_auth_token(user, secret_key: str, expiration: int = 600) -> bytes:
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': user.id})

    @staticmethod
    def verify_auth_token(token: str, secret_key: str) -> TokenState:
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return TokenState.Expired  # valid token, but expired
        except BadSignature:
            return TokenState.BadSignature  # invalid token
        return TokenState.Valid
