# pylint: disable=no-self-use

import logging.config

import regex

from flashback.logging import DEFAULT_CONSOLE_CONFIGURATION
from flashback.logging import DJANGO_CONSOLE_CONFIGURATION
from flashback.logging import FLASK_CONSOLE_CONFIGURATION
from flashback.logging import PYRAMID_CONSOLE_CONFIGURATION
from flashback.logging import RAILS_CONSOLE_CONFIGURATION


class TestConfigurations:
    CRE_DEFAULT_FORMAT = regex.compile(r"[\d- :,]{23} - tests.logging - MainProcess - INFO - message\n$")
    CRE_DJANGO_FORMAT = regex.compile(r"message\n$")
    CRE_FLASK_FORMAT = regex.compile(r"\[[\d- :,]{23}\] INFO in test_configurations: message\n$")
    CRE_PYRAMID_FORMAT = regex.compile(r"[\d- :,]{23} INFO  \[tests.logging:\d+\]\[MainThread\] message\n$")
    CRE_RAILS_FORMAT = regex.compile(r"I, \[[\d-T:\.]{23} #\d{1,4}\]     INFO -- : message\n$")

    def test_default_console_configuration(self, capsys):
        logging.config.dictConfig(DEFAULT_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        logger.info('message')

        captured = capsys.readouterr()
        print(captured)
        assert self.CRE_DEFAULT_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def test_django_console_configuration(self, capsys):
        logging.config.dictConfig(DJANGO_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        logger.info('message')

        captured = capsys.readouterr()
        assert self.CRE_DJANGO_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def test_flask_console_configuration(self, capsys):
        logging.config.dictConfig(FLASK_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        logger.info('message')

        captured = capsys.readouterr()
        assert self.CRE_FLASK_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def test_pyramid_console_configuration(self, capsys):
        logging.config.dictConfig(PYRAMID_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        logger.info('message')

        captured = capsys.readouterr()
        print(captured)
        assert self.CRE_PYRAMID_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def test_rails_console_configuration(self, capsys):
        logging.config.dictConfig(RAILS_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        logger.info('message')

        captured = capsys.readouterr()
        assert self.CRE_RAILS_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1
