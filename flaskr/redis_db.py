import redis


class RedisDB:
    def __init__(self, **connection_kwargs):
        connection_kwargs["decode_responses"] = True
        self.__pool = redis.ConnectionPool(**connection_kwargs)

    def save(self, key, data, ex=3600):
        r = redis.Redis(connection_pool=self.__pool)
        r.set(key, data, ex)

    def get(self, key):
        r = redis.Redis(connection_pool=self.__pool)
        return r.get(key)

    def delete(self, key):
        r = redis.Redis(connection_pool=self.__pool)
        r.delete(key)

    @property
    def pool(self):
        return self.__pool
