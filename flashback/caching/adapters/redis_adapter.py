from typing import Any, Hashable, Literal, Optional, Sequence, Tuple

from redis import Redis  # type: ignore
from redis.exceptions import *  # pylint: disable=unused-wildcard-import,wildcard-import,redefined-builtin
from redis.exceptions import ConnectionError as RedisConnectionError  # type: ignore
from redis.exceptions import ResponseError  # type: ignore
from redis.exceptions import TimeoutError as RedisTimeoutError  # type: ignore

from .base import BaseAdapter


class RedisAdapter(BaseAdapter):
    """
    Exposes a cache store using Redis.

    Exposes `redis`' exceptions, while renaming `redis.exceptions.ConnectionError` to
    `RedisConnectionError` and `redis.exceptions.TimeoutError` to `RedisTimeoutError`
    to avoid conflicts with builtin exceptions.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: str = "0", encoding: str = "utf-8", **kwargs: Any) -> None:
        super().__init__()

        # We would pass `decode_responses=True` to redis to avoid decoding in `get` and `batch_get`
        # but mockredis does not support it as of 2020-04-24
        self._encoding = encoding
        self.store = Redis(host=host, port=port, db=db, encoding=encoding, **kwargs)

    def set(self, key: Hashable, value: Any, ttl: int) -> bool:
        nulled_ttl = None if ttl == -1 else ttl

        return self.store.set(key, value, ex=nulled_ttl)

    def batch_set(self, keys: Sequence[Hashable], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        nulled_ttls = [None if ttl == -1 else ttl for ttl in ttls]

        pipe = self.store.pipeline()

        pipe.mset(dict(zip(keys, values)))
        for key, ttl in zip(keys, nulled_ttls):
            if ttl is not None:
                pipe.expire(key, ttl)

        return pipe.execute()

    def get(self, key: Hashable) -> Optional[Any]:
        value = self.store.get(key)

        return value.decode(self._encoding) if value is not None else None

    def batch_get(self, keys: Sequence[Hashable]) -> Sequence[Optional[Any]]:
        values = self.store.mget(keys)

        return [value.decode(self._encoding) if value is not None else None for value in values]

    def delete(self, key: Hashable) -> bool:
        return bool(self.store.delete(key))

    def batch_delete(self, keys: Sequence[Hashable]) -> bool:
        res = self.store.delete(*keys)

        return res == len(keys)

    def exists(self, key: Hashable) -> bool:
        return self.store.exists(key)

    def flush(self) -> Literal[True]:
        return self.store.flushdb()

    def ping(self) -> Literal[True]:
        return self.store.ping()

    @property
    def connection_exceptions(self) -> Tuple[Exception, ...]:
        return (RedisConnectionError, RedisTimeoutError, ResponseError)
