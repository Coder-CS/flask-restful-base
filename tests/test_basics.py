import sys

import pytest
from itsdangerous import BadSignature

sys.path.append(".")
from app.token import TokenState, Token


def test_token():
    key = "fasfas"
    token = Token.generate_token(key, 600, id=1)
    result = Token.verify_token(token, key)

    assert result == (TokenState.Valid, {"id":1})
    result2 = Token.verify_token("asfs", key)
    assert result2 == (TokenState.Invalid, {})

    token2 = Token.generate_token(key, -600)
    result3 = Token.verify_token(token2, key)
    assert result3 == (TokenState.Expired, {})