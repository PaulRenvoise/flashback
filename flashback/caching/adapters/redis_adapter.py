from collections.abc import Sequence
import typing as t

from redis import Redis
from redis.exceptions import *  # noqa: F403
from redis.exceptions import ResponseError as RedisResponseError
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

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        encoding: str = "utf-8",
        **kwargs,
    ) -> None:
        # We would pass `decode_responses=True` to redis to avoid decoding in `get` and `batch_get`
        # but mockredis does not support it as of 2020-04-24
        self._encoding = encoding
        self.store = Redis(host=host, port=port, db=db, encoding=encoding, **kwargs)

    def set(self, key: str, value: t.Any, ttl: int) -> bool:
        if ttl == -1:
            converted_ttl = None
        else:
            converted_ttl = ttl

        return self.store.set(key, value, ex=converted_ttl)  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def batch_set(self, keys: Sequence[str], values: Sequence[t.Any], ttls: Sequence[int]) -> bool:
        converted_ttls = [None if ttl == -1 else ttl for ttl in ttls]

        pipe = self.store.pipeline()

        pipe.mset(dict(zip(keys, values)))
        for key, ttl in zip(keys, converted_ttls):
            if ttl is not None:
                pipe.expire(key, ttl)

        return pipe.execute()  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def get(self, key: str) -> t.Any | None:
        value = self.store.get(key)

        return value.decode(self._encoding) if value is not None else None  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def batch_get(self, keys: Sequence[str]) -> Sequence[t.Any | None]:
        values = self.store.mget(keys)

        return [value.decode(self._encoding) if value is not None else None for value in values]  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def delete(self, key: str) -> bool:
        return bool(self.store.delete(key))

    def batch_delete(self, keys: Sequence[str]) -> bool:
        res = self.store.delete(*keys)

        return res == len(keys)

    def exists(self, key: str) -> bool:
        return self.store.exists(key)  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def flush(self) -> bool:
        return self.store.flushdb()  # type: ignore because redis command's return type is Awaitable[Any] | Any

    def ping(self) -> bool:
        return self.store.ping()  # type: ignore because redis command's return type is Awaitable[Any] | Any

    @property
    def connection_exceptions(self) -> tuple[type[Exception], ...]:
        return (RedisConnectionError, RedisTimeoutError, RedisResponseError)
