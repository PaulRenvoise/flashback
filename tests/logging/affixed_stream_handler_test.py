import io
import logging
import logging.config

from flashback.logging import AffixedStreamHandler


class AffixedStreamHandlerTest:
    def instance_usage_test(self) -> None:
        stream = io.StringIO()
        handler = AffixedStreamHandler(stream, prefix="__PREFIX__", suffix="__SUFFIX__")
        logger = logging.getLogger("instance_usage_test")
        logger.addHandler(handler)

        logger.error("error message")

        assert stream.getvalue() == "__PREFIX__error message__SUFFIX__"

    def dictconfig_usage_test(self) -> None:
        stream = io.StringIO()
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "incremental": False,
            "formatters": {},
            "filters": {},
            "handlers": {
                "stringio": {
                    "()": "flashback.logging.AffixedStreamHandler",
                    "stream": stream,
                    "prefix": "__START__",
                    "suffix": "__END__",
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "dictconfig_usage_test": {
                    "handlers": ["stringio"],
                    "level": "DEBUG",
                },
            },
        }
        logging.config.dictConfig(config)
        logger = logging.getLogger("dictconfig_usage_test")

        logger.info("info message")

        assert stream.getvalue() == "__START__info message__END__"
