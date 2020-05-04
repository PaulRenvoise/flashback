# pylint: disable=no-self-use

import io
import logging
import logging.config

from flashback.logging import AffixedStreamHandler


class TestAffixedStreamHandler:
    def test_instance_usage(self):
        stream = io.StringIO()
        handler = AffixedStreamHandler(stream, prefix='__PREFIX__', suffix='__SUFFIX__')
        logger = logging.getLogger('test_instance_usage')
        logger.addHandler(handler)

        logger.error('error message')

        assert stream.getvalue() == '__PREFIX__error message__SUFFIX__'

    def test_dictconfig_usage(self):
        stream = io.StringIO()
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'incremental': False,
            'formatters': {},
            'filters': {},
            'handlers': {
                'stringio': {
                    '()': 'flashback.logging.AffixedStreamHandler',
                    'stream': stream,
                    'prefix': '__START__',
                    'suffix': '__END__',
                    'level': 'DEBUG'
                }
            },
            'loggers': {
                'test_dictconfig_usage': {
                    'handlers': ['stringio'],
                    'level': 'DEBUG'
                }
            }
        }
        logging.config.dictConfig(config)
        logger = logging.getLogger('test_dictconfig_usage')

        logger.info('info message')

        assert stream.getvalue() == '__START__info message__END__'
