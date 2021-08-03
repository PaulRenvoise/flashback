import functools
import logging
from logging import getLogger, Logger


def muted(loggers=None):
    """
    Mutes all (or selected) loggers while executing a callable.

    By default, mute all loggers.

    Use 'None' as name for the root logger.

    Examples:
        ```python
        import logging
        from flashback.logging import muted

        logging.getLogger().setLevel(logging.INFO)
        how_logger = logging.getLogger("how")
        bye_logger = logging.getLogger("bye")

        def noisy_greetings():
            logging.info("Hi")
            how_logger.info("How are you?")
            bye_logger.info("Bye")

        noisy_greetings()
        #=> "Hi"
        #=> "How are you?"
        #=> "Bye"

        # You can mute specific loggers with their names,
        # their instance, or 'None' for the root logger
        @muted(loggers=["how", bye_logger, None])
        def quiet_greetings():
            logging.info("Hi")
            how_logger.info("How are you?")
            bye_logger.info("Bye")

        quiet_greetings()

        # Or mute all (including root) loggers
        @muted()
        def muted_greetings():
            logging.info("Hi")
            how_logger.info("How are you?")
            bye_logger.info("Bye")

        muted_greetings()
        ```

    Params:
        loggers (Iterable<str|logging.Logger>): the list of logger names or instances to mute

    Returns:
        Callable: a wrapper used to decorate a callable
    """
    def wrapper(func):
        def _filter(_record):
            return False

        @functools.wraps(func)
        def inner(*args, **kwargs):
            # Selects all loggers at each call to func because loggers can be created between calls
            if loggers is None:
                selected_loggers = [getLogger(logger) for logger in logging.root.manager.loggerDict] + [logging.root] # pylint: disable=no-member
            else:
                selected_loggers = [logger if isinstance(logger, Logger) else getLogger(logger) for logger in loggers]

            for logger in selected_loggers:
                logger.addFilter(_filter)

            result = func(*args, **kwargs)

            for logger in selected_loggers:
                logger.removeFilter(_filter)

            return result

        return inner

    return wrapper
