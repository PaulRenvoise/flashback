from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """
    Defines an abstract adapter which needs to be implemented to register a new adapter.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Instanciates the adapter, without testing the connection (ping is used for that).

        Params:
            - `kwargs (dict)` every given keyword arguments

        Returns:
            - `copernicus.caching.adapters.base.BaseAdapter` an instance of the caching adapter
        """

    @abstractmethod
    def set(self, key, value, ttl):
        """
        Caches a `value` under a given `key`.

        Params:
            - `key (str)` the key under which to cache the value
            - `value (str)` the value to cache
            - `ttl (int)` the number of seconds after which the record must be evicted

        Returns:
            - `bool` whether or not the operation succeeded

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def batch_set(self, keys, values, ttl):
        """
        Caches each value from a list of values to its respective key in a list of keys.

        Params:
            - `keys (Iterable<str>)` the keys under which to cache the values
            - `values (Iterable<str>)` the values to cache
            - `ttl (Iterable<int>)` the list of time to live of each record

        Returns:
            - `bool` whether or not the operation succeeded

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
            - `ValueError` if the lengths of keys and values differ
        """

    @abstractmethod
    def get(self, key):
        """
        Fetches the value stored under `key`.

        Params:
            - `key (str)` the key to retreive the value from

        Returns:
            - `str|None` the value read from the cache

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def batch_get(self, keys):
        """
        Fetches each value stored under its respective key in a list of `keys`.

        Params:
            - `keys (Iterable<str>)` the keys to retreive the values from

        Returns:
            - `list<str|None>` the values read from the cache

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def delete(self, key):
        """
        Removes the given cache `key`.

        Params:
            - `key (str)` the key to remove

        Returns:
            - `bool` whether or not the operation succeeded

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def batch_delete(self, keys):
        """
        Removes the cache of a given list of keys, ignores non-existing keys.

        Params:
            - `keys (Iterable<str>)` the keys to remove from the cache

        Returns:
            - `bool` whether or not the operation succeeded

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def exists(self, key):
        """
        Checks the existence of a given key.

        Params:
            - `key (str)` the key to check the existence of

        Returns:
            - `bool` whether or not the key exists

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def flush(self):
        """
        Flushes all keys and values from the adapter's store.

        Params:
            - `None`

        Returns:
            - `bool` always True

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @abstractmethod
    def ping(self):
        """
        Checks if a valid connection is setup with the cache store.

        Params:
            - `None`

        Returns:
            - `bool` always True

        Raises:
            - `Base.connection_exceptions` if no connection to the underlying cache system is active
        """

    @property
    @abstractmethod
    def connection_exceptions(self):
        """
        Lists the exceptions raised by the adapter in case of a faulty, busy, etc. connection to the storage.

        Params:
            - `None`

        Returns:
            - `tuple<Exception>` the list of exceptions
        """
