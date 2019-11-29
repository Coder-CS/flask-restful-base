import redis


class RedisDB:
    def __init__(self, **connection_kwargs):
        connection_kwargs["decode_responses"] = True
        self.__pool = redis.ConnectionPool(**connection_kwargs)
        self.__redis = redis.Redis(connection_pool=self.__pool)

    def set(self, key, data, ex=3600):
        self.__redis.set(key, data, ex)

    def get(self, key):
        return self.__redis.get(key)

    def delete(self, key):
        self.__redis.delete(key)

    @property
    def pool(self):
        return self.__pool
