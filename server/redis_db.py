import redis


class RedisDB(object):
    """对 redis 封装.

        用于操作 redis.

    """
    def __init__(self, **connection_kwargs):
        """ 初始化.

        :param connection_kwargs: 需要四个参数 ip, port, password, db
        """
        connection_kwargs["decode_responses"] = True
        self.__pool = redis.ConnectionPool(**connection_kwargs)
        self.__redis = redis.Redis(connection_pool=self.__pool)

    def __del__(self):
        self.__pool.disconnect()
        self.__redis.close()

    def set(self, key, data, ex=3600) -> bool:
        return self.__redis.set(key, data, ex)

    def get(self, key):
        return self.__redis.get(key)

    def delete(self, key) -> int:
        return self.__redis.delete(key)

    @property
    def pool(self):
        return self.__pool
