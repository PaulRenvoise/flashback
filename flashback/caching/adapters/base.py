from abc import ABC, abstractmethod
from typing import Any, Hashable, Literal, Optional, Sequence, Tuple


class BaseAdapter(ABC):
    """
    Defines an abstract class that needs to be implemented to register a new adapter.
    """
    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Instanciates the adapter, without testing the connection (ping is used for that).

        Params:
            kwargs: every given keyword arguments
        """

    @abstractmethod
    def set(self, key: Hashable, value: Any, ttl: int) -> bool:
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
    def batch_set(self, keys: Sequence[Hashable], values: Sequence[Any], ttls: Sequence[int]) -> bool:
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
    def get(self, key: Hashable) -> Optional[Any]:
        """
        Fetches the value stored under `key`.

        Params:
            key (str): the key to retreive the value from

        Returns:
            str|None: the value read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_get(self, keys: Sequence[Hashable]) -> Sequence[Optional[Any]]:
        """
        Fetches each value stored under its respective key in a list of `keys`.

        Params:
            keys (Iterable<str>): the keys to retreive the values from

        Returns:
            list<str|None>: the values read from the cache

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def delete(self, key: Hashable) -> bool:
        """
        Removes the given cache `key`.

        Params:
            key (str): the key to remove

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def batch_delete(self, keys: Sequence[Hashable]) -> bool:
        """
        Removes the cache of a given list of `keys`, ignores non-existing keys.

        Params:
            keys (Iterable<str>): the keys to remove from the cache

        Returns:
            bool: whether or not the operation succeeded

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def exists(self, key: Hashable) -> bool:
        """
        Checks the existence of a given `key` in the storage.

        Params:
            key (str): the key to check the existence of

        Returns:
            bool: whether or not the key exists

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def flush(self) -> Literal[True]:
        """
        Flushes all keys and values from the adapter's storage.

        Returns:
            bool: always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @abstractmethod
    def ping(self) -> Literal[True]:
        """
        Checks if a valid connection is setup with the underlying storage.

        Returns:
            bool: always True

        Raises:
            Base.connection_exceptions: if no connection to the underlying storage is active
        """

    @property
    @abstractmethod
    def connection_exceptions(self) -> Tuple[Exception, ...]:
        """
        Lists the exceptions raised by the adapter when a faulty/invalid connection is detected.

        Returns:
            tuple<Exception>: the list of exceptions
        """
