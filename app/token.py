from enum import Enum
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class TokenState(Enum):
    Expired = 1
    Invalid = 2
    Valid = 3


class Token(object):
    @staticmethod
    def generate_token(secret_key: str, expiration: int = 600, **kwargs) -> bytes:
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({**kwargs})

    @staticmethod
    def verify_token(token: str, secret_key: str) -> (TokenState, dict):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return TokenState.Expired, {}  # valid token, but expired
        except BadSignature:
            return TokenState.Invalid, {}  # invalid token
        return TokenState.Valid, data
