import re


def is_valid_email(email: str) -> bool:
    test = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    ret = re.match(test, email)
    if ret:
        return True
    return False
