import time
from enum import Enum
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class TokenState(Enum):
    Expired = 1
    Invalid = 2
    Valid = 3


class Token(object):
    @staticmethod
    def generate_token(id, secret_key: str, expiration: int = 600, **kwargs) -> str:
        s = Serializer(secret_key, expires_in=expiration)
        return str(s.dumps({"id": id, "time": time.time(), **kwargs}), "utf-8")

    @staticmethod
    def verify_token(token: str, secret_key: str) -> (TokenState, dict):
        s = Serializer(secret_key)
        try:
            token_byte = bytes(token, "utf8")
            data = s.loads(token_byte)
        except SignatureExpired:
            return TokenState.Expired, {}  # valid token, but expired
        except BadSignature:
            return TokenState.Invalid, {}  # invalid token
        return TokenState.Valid, data
