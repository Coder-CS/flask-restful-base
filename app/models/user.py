import datetime
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from werkzeug.security import check_password_hash, generate_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, secret_key: str, expiration: int = 600) -> bytes:
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token: str, secret_key: str) -> int:
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return -1  # valid token, but expired
        except BadSignature:
            return -1  # invalid token
        return data.get('id', -1)

