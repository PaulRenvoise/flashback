# pylint: disable=no-self-use

import logging.config

from flashback.logging import DEFAULT_CONSOLE_CONFIGURATION
from flashback.logging import RAILS_CONSOLE_CONFIGURATION


class TestConfigurations:
    def test_default_console_configuration(self):
        handler_class = DEFAULT_CONSOLE_CONFIGURATION['handlers']['console']['class']
        formatter_format = DEFAULT_CONSOLE_CONFIGURATION['formatters']['default']['format']

        logging.config.dictConfig(DEFAULT_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        assert logger.level == 10
        assert len(logger.handlers) == 1

        handler = logger.handlers[0]
        assert f"{handler.__module__}.{handler.__class__.__name__}" == handler_class
        assert handler.formatter._fmt == formatter_format  # pylint: disable=protected-access

    def test_rails_console_configuration(self):
        handler_class = RAILS_CONSOLE_CONFIGURATION['handlers']['console']['class']
        formatter_format = RAILS_CONSOLE_CONFIGURATION['formatters']['default']['format']

        logging.config.dictConfig(RAILS_CONSOLE_CONFIGURATION)

        logger = logging.getLogger('tests.logging')

        assert logger.level == 10
        assert len(logger.handlers) == 1

        handler = logger.handlers[0]
        assert f"{handler.__module__}.{handler.__class__.__name__}" == handler_class
        assert handler.formatter._fmt == formatter_format  # pylint: disable=protected-access
