import unittest
from app.redis_db import RedisDB

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
        self.assertEqual(self.db.set(1, "a"), True)
        self.assertEqual(self.db.set(1, "c"), True)
        self.assertEqual(self.db.set("1", "b"), True)
        b = self.db.get(1)
        c = self.db.get("1")
        self.assertEqual(b, "b")
        self.assertEqual(b, c)

    def test_delete(self):
        self.db.set(3, "3a")
        self.assertEqual(self.db.delete(3), 1)
        self.assertEqual(self.db.delete(3), 0)
        self.assertEqual(self.db.delete(3), 0)
        a = self.db.get(3)
        self.assertIsNone(a)

    def test_close(self):
        self.assertIsNone(self.db.__del__())