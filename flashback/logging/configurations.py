import inspect


# Dynamically sets the top-level logger configuration by extrating the package name from the module importing this file.
# This avoids the behavior where ALL libraries would have the defined logging level if we use the 'root' key.
#
# The con of this method is that the indices used to access the stack are hardcoded,
# meaning that the importing line must look like the following, else we won't have a package:
# ```
# from corpernicus.logging import DEFAULT_CONSOLE_CONFIGURATION
# ```
try:
    IMPORTER = inspect.getmodule(inspect.stack()[12][0]).__package__ or 'flashback'
except (IndexError, AttributeError):
    IMPORTER = 'flashback'


DEFAULT_CONSOLE_CONFIGURATION = {
    'version': 1,
    'disable_existing_loggers': True,
    'incremental': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(processName)s - %(levelname)s - %(message)s'
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        IMPORTER: {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}


RAILS_CONSOLE_CONFIGURATION = {
    'version': 1,
    'disable_existing_loggers': True,
    'incremental': False,
    'formatters': {
        'default': {
            'format': '%(levelname)1.1s, [%(asctime)s.%(msecs)03d #%(process)d] %(levelname)8s -- : %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        IMPORTER: {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}
