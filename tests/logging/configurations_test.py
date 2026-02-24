import logging.config

import pytest
import regex

from flashback.logging import DEFAULT_CONSOLE_CONFIGURATION
from flashback.logging import DJANGO_CONSOLE_CONFIGURATION
from flashback.logging import FLASK_CONSOLE_CONFIGURATION
from flashback.logging import PYRAMID_CONSOLE_CONFIGURATION
from flashback.logging import RAILS_CONSOLE_CONFIGURATION


class ConfigurationsTest:
    CRE_DEFAULT_FORMAT = regex.compile(r"[\d- :,]{23} - tests.logging - [^\s]+ - INFO - message\n$")
    CRE_DJANGO_FORMAT = regex.compile(r"message\n$")
    CRE_FLASK_FORMAT = regex.compile(r"\[[\d- :,]{23}\] INFO in configurations_test: message\n$")
    CRE_PYRAMID_FORMAT = regex.compile(r"[\d- :,]{23} INFO  \[tests.logging:\d+\]\[[^\s]+\] message\n$")
    CRE_RAILS_FORMAT = regex.compile(r"I, \[[\d-T:\.]{23} #\d+\]     INFO -- : message\n$")

    def default_console_configuration_test(self, capsys: pytest.CaptureFixture) -> None:
        logging.config.dictConfig(DEFAULT_CONSOLE_CONFIGURATION)

        logger = logging.getLogger("tests.logging")

        logger.info("message")

        captured = capsys.readouterr()
        assert self.CRE_DEFAULT_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def django_console_configuration_test(self, capsys: pytest.CaptureFixture) -> None:
        logging.config.dictConfig(DJANGO_CONSOLE_CONFIGURATION)

        logger = logging.getLogger("tests.logging")

        logger.info("message")

        captured = capsys.readouterr()
        assert self.CRE_DJANGO_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def flask_console_configuration_test(self, capsys: pytest.CaptureFixture) -> None:
        logging.config.dictConfig(FLASK_CONSOLE_CONFIGURATION)

        logger = logging.getLogger("tests.logging")

        logger.info("message")

        captured = capsys.readouterr()
        assert self.CRE_FLASK_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def pyramid_console_configuration_test(self, capsys: pytest.CaptureFixture) -> None:
        logging.config.dictConfig(PYRAMID_CONSOLE_CONFIGURATION)

        logger = logging.getLogger("tests.logging")

        logger.info("message")

        captured = capsys.readouterr()
        assert self.CRE_PYRAMID_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1

    def rails_console_configuration_test(self, capsys: pytest.CaptureFixture) -> None:
        logging.config.dictConfig(RAILS_CONSOLE_CONFIGURATION)

        logger = logging.getLogger("tests.logging")

        logger.info("message")

        captured = capsys.readouterr()
        assert self.CRE_RAILS_FORMAT.match(captured.err)

        assert logger.level == 10
        assert len(logger.handlers) == 1
