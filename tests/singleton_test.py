import typing as t

from flashback import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, name) -> None:
        self.name = name


class LooseLogger(metaclass=Singleton, strict=False):
    def __init__(self, name) -> None:
        self.name = name


class SingletonTest:
    def simple_test(self) -> None:
        logger_1 = Logger("db")
        logger_2 = Logger("auth")
        logger_3 = Logger("db")

        assert logger_1 != logger_2
        assert logger_1 == logger_3
        assert logger_1 is logger_3

    def loose_test(self) -> None:
        logger_1 = LooseLogger("db")
        logger_2 = LooseLogger("auth")
        logger_3 = LooseLogger("db")

        assert logger_1 == logger_2
        assert logger_1 is logger_2
        assert logger_1 == logger_3
        assert logger_1 is logger_3

    def metaclass_none_namespace_and_attributes_test(self) -> None:
        cls = t.cast("Singleton", Singleton.__new__(Singleton, "MetaOnly", (object,), None))
        Singleton.__init__(cls, "MetaOnly", (object,), None)

        assert cls.strict is True
        assert cls._instances == {}
