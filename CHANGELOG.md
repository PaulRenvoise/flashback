# Changelog

## 1.0.0 (TBD)

- Added the `caching/` module, containing caching helpers:
    - A wrapper supporting several cache stores: in-memory, disk, Redis, and Memcached
    - A decorator `@cacheable`, that caches a callable's return value based on its arguments
- Added the `debugging/` module:
    - A helper function `xp`, to print debugging statements
- Added the `formatting/` module, a collection of helper functions:
    - `oxford_join()` joins strings in a human-readable way
    - `transliterate()` represents unicode text in ASCII (using [Unidecode](https://github.com/avian2/unidecode))
    - `camelize()` transforms any-case to CamelCase
    - `snakeize()` transforms any-case to snake\_case
    - `parameterize()` formats a given string to be used in URLs
    - `ordinalize()` represents numbers in their ordinal representations
    - `adverbize()` represents numbers in their numeral adverb representations
    - `truncate()` truncates long sentences at a given limit and append a suffix if needed
    - `singularize()` returns the singular form of a given word
    - `pluralize()` returns the plural form of a given word
- Added the `i16g/` module, to help with locale management:
    - A helper class to dynamically load localization files from a package path
- Added the `importing/` module, a collection of helpers for dynamic importing:
    - `import_class_from_path()` fetches a class from a package path and returns it
    - `import_module_from_path()` exposes the contents of a module as globals from a package path
- Added the `logging/` module, containing drop-in configuration for the logging module:
    - `DEFAULT_CONSOLE_CONFIGURATION` uses the default formatting to log in the console
    - `RAILS_CONSOLE_CONFIGURATION` formats logs in a RoR-way before routing them to the console
- Added `Borg`, a design pattern to produce a singleton behaviour across multiple instances of a class
- Added `@classproperty`, to combine @classmethod and @property
- Added `@deprecated`, to flag deprecated callables with a explicit message
- Added `@retryable`, to retry failing executing of a callable
- Added `@timeable`, to measure the execution time of a callable
- Added `@sampled`, implementing 3 sampling strategies to filter calls made to a callable:
    - constant: Limits, or not, all calls received
    - probabilistic: Limits the number of calls to a ratio of accepted/refused calls
    - ratelimiting: Limits the number of calls to a fixed rate per second
- Added `@timeoutable`, stopping the execution of a callable if its run time is too long
