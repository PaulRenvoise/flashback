# pylint: disable=no-self-use,redefined-outer-name

import io
import logging

import pytest

from flashback.logging import muted


logging.getLogger().setLevel(logging.DEBUG)
LOGGER_1 = logging.getLogger('logger_1')
LOGGER_2 = logging.getLogger('logger_2')
LOGGER_3 = logging.getLogger('logger_3')

@pytest.fixture(autouse=True)
def clean_up_loggers():
    for logger in [LOGGER_1, LOGGER_2, LOGGER_3]:
        for handler in logger.handlers:
            logger.removeHandler(handler)


@pytest.fixture
def stream():
    stream = io.StringIO()

    for logger in [logging.root, LOGGER_1, LOGGER_2, LOGGER_3]:
        logger.addHandler(logging.StreamHandler(stream))

    return stream


def dummy_func():
    logging.info('root')
    LOGGER_1.info('logger_1')
    LOGGER_2.info('logger_2')
    LOGGER_3.info('logger_3')


class TestMuted:
    def test_muted(self, stream):
        make_muted = muted()
        decorated_func = make_muted(dummy_func)

        decorated_func()

        assert stream.getvalue() == ''

    def test_muted_str(self, stream):
        make_muted = muted(loggers=['logger_1'])
        decorated_func = make_muted(dummy_func)

        decorated_func()

        value = stream.getvalue()
        assert 'root' in value
        assert 'logger_1' not in value
        assert 'logger_2' in value
        assert 'logger_3' in value

    def test_muted_none(self, stream):
        make_muted = muted(loggers=[None])
        decorated_func = make_muted(dummy_func)

        decorated_func()

        value = stream.getvalue()
        assert 'root' not in value
        assert 'logger_1' in value
        assert 'logger_2' in value
        assert 'logger_3' in value

    def test_muted_logger(self, stream):
        make_muted = muted(loggers=[LOGGER_2])
        decorated_func = make_muted(dummy_func)

        decorated_func()

        value = stream.getvalue()
        assert 'root' in value
        assert 'logger_1' in value
        assert 'logger_2' not in value
        assert 'logger_3' in value

    def test_muted_mixed(self, stream):
        make_muted = muted(loggers=[None, 'logger_1', LOGGER_2])
        decorated_func = make_muted(dummy_func)

        decorated_func()

        value = stream.getvalue()
        assert 'root' not in value
        assert 'logger_1' not in value
        assert 'logger_2' not in value
        assert 'logger_3' in value
