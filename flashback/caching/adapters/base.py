from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class BaseAdapter(ABC):
    """
    Defines an abstract class that needs to be implemented to register a new adapter.
    """

    @abstractmethod
    def __init__(self, **kwargs) -> None:
        """
        Instanciates the adapter, without testing the connection (ping is used for that).

        Params:
            kwargs: every given keyword arguments
        """

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> bool:
        """
        Caches a `value` under a given `key`.

        Params:
            key: the key under which to cache the value
            value: the value to cache
            ttl: the number of seconds before expiring the key

        Returns:
            whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_set(self, keys: Sequence[str], values: Sequence[Any], ttls: Sequence[int]) -> bool:
        """
        Caches each value from a list of `values` to its respective key in a list of `keys`.

        Params:
            keys: the keys under which to cache the values
            values: the values to cache
            ttls: the number of seconds before expiring the keys

        Returns:
            whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """
        Fetches the value stored under `key`.

        Params:
            key: the key to retreive the value from

        Returns:
            the value read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_get(self, keys: Sequence[str]) -> Sequence[Any | None]:
        """
        Fetches each value stored under its respective key in a list of `keys`.

        Params:
            keys: the keys to retreive the values from

        Returns:
            the values read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Removes the given cache `key`.

        Params:
            key: the key to remove

        Returns:
            whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_delete(self, keys: Sequence[str]) -> bool:
        """
        Removes the cache of a given list of `keys`, ignores non-existing keys.

        Params:
            keys: the keys to remove from the cache

        Returns:
            whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Checks the existence of a given `key` in the storage.

        Params:
            key (str): the key to check the existence of

        Returns:
            whether or not the key exists

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def flush(self) -> bool:
        """
        Flushes all keys and values from the adapter's storage.

        Returns:
            always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def ping(self) -> bool:
        """
        Checks if a valid connection is setup with the underlying storage.

        Returns:
            always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @property
    @abstractmethod
    def connection_exceptions(self) -> tuple[Exception, ...]:
        """
        Lists the exceptions raised by the adapter when a faulty/invalid connection is detected.

        Returns:
            tuple<Exception>: the list of exceptions
        """
