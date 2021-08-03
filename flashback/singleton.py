import functools


class Singleton(type):
    """
    Implements a Singleton metaclass.

    Any class using this metaclass can be made strict or not.
    If the strict behavior is enforced, only one instance will be created for each group of
    positional and keyword arguments given to the class' constructor. Else, only one instance will
    be created. By default, the strict behavior is enforced.

    Relies on the key building mechanism from `functools._make_key` to hash the positional and
    keywords arguments.

    Examples:
        ```python
        from flashback import Singleton

        class Logger(metaclass=Singleton):
            def __init__(self, name):
                self.name = name

        logger_1 = Logger("db")
        logger_2 = Logger("auth")
        logger_3 = Logger("db")

        assert logger_1 != logger_2
        assert logger_1 == logger_3
        assert logger_1 is logger_3

        class LooseLogger(metaclass=Singleton, strict=False):
            def __init__(self, name):
                self.name = name

        loose_logger_1 = LooseLogger("db")
        loose_logger_2 = LooseLogger("auth")

        assert loose_logger_1 == loose_logger_2
        assert loose_logger_1 is loose_logger_2

        assert logger_1 != loose_logger_1
        ```
    """
    def __new__(cls, name, bases, namespace, **_kwargs):
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, attributes, strict=True):
        """
        Params:
            name (str): the name of the class to initialize
            bases (tuple): the bases classes of the class
            attributes (dict): the internal __dict__ of the class
            strict (bool): whether or not to enforce the strict behavior for singleton creation
        """
        super().__init__(name, bases, attributes)

        cls.strict = strict
        cls._instances = {}

    def __call__(cls, *args, **kwargs):
        if cls.strict:
            key = functools._make_key(args, kwargs, True)  # pylint: disable=protected-access
        else:
            key = 0

        instance = cls._instances.get(key, None)
        if instance is None:
            instance = super().__call__(*args, **kwargs)

            cls._instances[key] = instance

        return instance
