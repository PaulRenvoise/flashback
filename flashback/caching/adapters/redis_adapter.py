from redis import Redis
from redis.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import,redefined-builtin
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError

from .base import BaseAdapter


class RedisAdapter(BaseAdapter):
    """
    Exposes a cache store using Redis.

    Exposes `redis`' exceptions, while renaming `redis.exceptions.ConnectionError` to
    `RedisConnectionError` and `redis.exceptions.TimeoutError` to `RedisTimeoutError`
    to avoid conflicts with builtin exceptions.
    """

    def __init__(self, host="localhost", port=6379, db="0", encoding="utf-8", **kwargs):
        super().__init__()

        # We would pass `decode_responses=True` to redis to avoid decoding in `get` and `batch_get`
        # but mockredis does not support it as of 2020-04-24
        self._encoding = encoding
        self.store = Redis(host=host, port=port, db=db, encoding=encoding, **kwargs)

    def set(self, key, value, ttl):
        if ttl == -1:
            ttl = None

        return self.store.set(key, value, ex=ttl)

    def batch_set(self, keys, values, ttls):
        ttls = [None if ttl == -1 else ttl for ttl in ttls]

        pipe = self.store.pipeline()

        pipe.mset(dict(zip(keys, values)))
        for key, ttl in zip(keys, ttls):
            if ttl is not None:
                pipe.expire(key, ttl)

        return pipe.execute()

    def get(self, key):
        value = self.store.get(key)

        return value.decode(self._encoding) if value is not None else None

    def batch_get(self, keys):
        values = self.store.mget(keys)

        return [value.decode(self._encoding) if value is not None else None for value in values]

    def delete(self, key):
        return bool(self.store.delete(key))

    def batch_delete(self, keys):
        res = self.store.delete(*keys)

        return res == len(keys)

    def exists(self, key):
        return self.store.exists(key)

    def flush(self):
        return self.store.flushdb()

    def ping(self):
        return self.store.ping()

    @property
    def connection_exceptions(self):
        return (RedisConnectionError, RedisTimeoutError, ResponseError)
