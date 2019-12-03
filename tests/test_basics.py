import sys

import pytest
from itsdangerous import BadSignature

sys.path.append(".")
from flaskr.token import TokenState, Token


def test_token():
    key = "fasfas"
    token = Token.generate_token(1, key, 600,)
    result = Token.verify_token(token, key)

    assert result[1]["id"] == 1
    result2 = Token.verify_token("asfs", key)
    assert result2[0] == TokenState.Invalid

    token2 = Token.generate_token(1, key, -600)
    result3 = Token.verify_token(token2, key)
    assert result3[0] == TokenState.Expired
