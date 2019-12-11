from werkzeug.security import check_password_hash, generate_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def __init__(self, account: str, name: str, password: str):
        self.account = account
        self.name = name
        self.password = password

    @staticmethod
    def add(account: str, name: str, password: str):
        user = User(account, name, password)
        db.session.add(user)
        db.session.commit()
        return user

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


