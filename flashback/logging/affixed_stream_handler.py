import logging


class AffixedStreamHandler(logging.StreamHandler):
    """
    Implements a custom handler that adds customizable prefix and suffix to the formatted record.

    This allows logging without trailing newlines, logs that are overwriting themselves (with ANSI
    escape-codes), or more complex behaviours.

    Examples:
        ```python
        import io
        import logging
        import logging.config
        from flashback.logging import AffixedStreamHandler

        # Usable via object configuration
        first_stream = io.StringIO()
        handler = AffixedStreamHandler(first_stream, prefix="_PREFIX_", suffix="_SUFFIX_")
        logger = logging.getLogger("first")
        logger.addHandler(handler)

        logger.error("error message")

        first_stream.getvalue()
        #=> "_PREFIX_error message_SUFFIX_"

        # But also via dictConfig
        second_stream = io.StringIO()
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "incremental": False,
            "formatters": {},
            "filters": {},
            "handlers": {
                "stringio": {
                    "()": "flashback.logging.AffixedStreamHandler",
                    "stream": second_stream,
                    "prefix": "_START_",
                    "suffix": "_END_",
                    "level": "DEBUG"
                }
            },
            "loggers": {
                "second": {
                    "handlers": ["stringio"],
                    "level": "DEBUG"
                }
            }
        }
        logging.config.dictConfig(config)
        logger = logging.getLogger("second")

        logger.info("info message")

        second_stream.getvalue()
        #=> "_START_info message_END_"
        ```
    """
    def __init__(self, stream=None, prefix="", suffix="\n"):
        """
        If stream is not specified, sys.stderr is used.

        Params:
            stream (TextIOWrapper): the stream to write to
            prefix (str): the prefix to prepend to the record
            suffix (str): the suffix to append to the record
        """
        super().__init__(stream=stream)

        self.prefix = prefix
        self.suffix = suffix

    def emit(self, record):
        """
        Writes a record to the stream after formatting it and affixing it with the configured
        prefix and suffix.

        If exception information is present, it is formatted using traceback.print_exception
        and appended to the stream. If the stream has an `encoding` attribute, it is used to
        determine how to do the output to the stream.

        Params:
            record (logging.LogRecord): the record to format and write

        Raises:
            RecursionError: if the maximum recursion depth is reached
        """
        try:
            msg = self.format(record)
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            stream.write(self.prefix + msg + self.suffix)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
