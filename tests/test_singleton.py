# pylint: disable=no-self-use

from flashback import Singleton


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

class LooseLogger(metaclass=Singleton, strict=False):
    def __init__(self, name):
        self.name = name

class TestSingleton:
    def test_singleton(self):
        logger_1 = Logger('db')
        logger_2 = Logger('auth')
        logger_3 = Logger('db')

        assert logger_1 != logger_2
        assert logger_1 == logger_3
        assert logger_1 is logger_3

    def test_loose_singleton(self):
        logger_1 = LooseLogger('db')
        logger_2 = LooseLogger('auth')
        logger_3 = LooseLogger('db')

        assert logger_1 == logger_2
        assert logger_1 is logger_2
        assert logger_1 == logger_3
        assert logger_1 is logger_3
