import unittest
from flaskr.redis_db import RedisDB

redis_config = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "password": None
}


# @unittest.skip("打开Redis再测试")
class RedisTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = RedisDB(**redis_config)

    def tearDown(self) -> None:
        self.db.pool.disconnect()

    def test_save_get(self):
        self.db.set(1, "a")
        self.db.set("1", "b")
        b = self.db.get(1)
        c = self.db.get("1")
        assert b == "b"
        assert b == c

    def test_delete(self):
        self.db.set(3, "3a")
        self.db.delete(3)
        self.db.delete(3)
        self.db.delete(3)
        self.db.delete(3)
        a = self.db.get(3)
        assert a == None