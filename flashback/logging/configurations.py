"""
Defines several logging configuration to use with `logging.config.dictConfig`.

Upon import, it dynamically extracts the package name from the module importing this file,
and sets the package name as top-level logger. This avoids the behavior where ALL libraries
would have the defined logging level if we use the 'root' key.
If the import is not done within a package (e.g. within a simple python script that is then
executed), it falls back to 'None', thus applying the configuration to the 'root' logger.

The con of this method is that the indices used to access the stack are hardcoded,
meaning that the importing line must look like the following, else it won't find a package:
```python
from flashback.logging import DEFAULT_CONSOLE_CONFIGURATION
```

`disable_existing_loggers` is set to false for each configuration because it breaks the loggers
created after using the configuration (see: https://gist.github.com/alanbriolat/d5ffe608b56c948533c6).
"""
import inspect

from ..debugging import get_frameinfo

try:
    IMPORTER = inspect.getmodule(get_frameinfo(12).frame).__package__ or None
except (IndexError, AttributeError):
    IMPORTER = None

DEFAULT_CONSOLE_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(processName)s - %(levelname)s - %(message)s"
        }
    },
    "filters": {},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        IMPORTER: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
"""
A simple logger applicable for most logging context.

Logs to stderr without filtering, and formats the message with `asctime`, `name`, `processName`,
`levelname`, and `message`.
"""

DJANGO_CONSOLE_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "formatters": {},
    "filters": {},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        IMPORTER: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
"""
A Django-like logger (which basically does nothing).

Logs to stderr without filtering, and formats the message with the default logging formatter.
"""

FLASK_CONSOLE_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "filters": {},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        IMPORTER: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
"""
A Flask-like logger.

Logs to stderr without filtering, and formats the message with `asctime`, `levelname`, `module`,
and `message`.
"""

PYRAMID_CONSOLE_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s"
        }
    },
    "filters": {},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        IMPORTER: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
"""
A Pyramid-like logger.

Logs to stderr without filtering, and formats the message with `asctime`, `levelname`, `name`,
`lineno`, `threadName`, and `message`.
"""

RAILS_CONSOLE_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": False,
    "formatters": {
        "default": {
            "format": "%(levelname)1.1s, [%(asctime)s.%(msecs)03d #%(process)d] %(levelname)8s -- : %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S"
        }
    },
    "filters": {},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "loggers": {
        IMPORTER: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
"""
A Ruby-on-Rails-like logger.

Logs to stderr without filtering, and formats the message with `asctime`, `msec`, `process`,
`levelname`, and `message`.
"""
