import sys

sys.path.append(".")
from commands import app, init_db, add_user


def test_command():
    runner = app.test_cli_runner()
    runner.invoke(init_db)

    name = "testName"
    result = runner.invoke(add_user, args=["asfs@qq.com", name, "asfsfsfas123"])

    assert result
