from werkzeug.security import check_password_hash, generate_password_hash
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def __init__(self, email: str, name: str, password: str):
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def add_user(email: str, name: str, password: str):
        user = User(email, name, password)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


