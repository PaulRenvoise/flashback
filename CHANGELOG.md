# Changelog

## 1.2.0 (02/10/2021)

- Fixed `iterating/uniq()` by using the `repr()` of each item to handle unhashable types
- Fixed `iterating/flatten()` to handle strings
- Updated dependencies
- Marked the project as "Production/Stable" on PyPI
- Switched pdoc3 for mkdocs
- Migrated from single and double quotes to double quotes only
- Added `iterating/flat_map()`, that applies a function to every item and nested item of the given iterable
- Removed all "# coding: utf-8" headers, since they're actually useless

## 1.1.0 (06/06/2021)

- Added the `accessing/` module, containing helpers to access values in maps and iterables:
    - `dig()` repeatedly access keys to find a nested value within a dict

## 1.0.0 (21/11/2020)

- Added the `caching/` module, containing caching helpers:
    - `Cache` supports several cache stores: in-memory, disk, Redis, and Memcached
    - `@cached` caches a callable's return value based on its arguments
- Added the `debugging/` module:
    - `xp()` prints debug information about its given arguments
    - `@profiled` collects and dumps profiling stats over a callable's execution
    - `caller()` allows a developer to print debug information about a callable's caller
    - `get_callable()` extracts a callable instance from a frame
    - `get_call_context()` finds and returning the code context around a call made in a frame
    - `get_frameinfo()` implements a faster `inspect.stack()[x]`
- Added the `formatting/` module, a collection of helper functions:
    - `oxford_join()` joins strings in a human-readable way
    - `transliterate()` represents unicode text in ASCII (using [Unidecode](https://github.com/avian2/unidecode))
    - `camelize()` transforms any case to camelCase
    - `pascalize()` transforms any case to PascalCase
    - `snakeize()` transforms any case to snake\_case
    - `kebabize()` transforms any case to kebab-case
    - `parameterize()` formats a given string to be used in URLs
    - `ordinalize()` represents numbers in their ordinal representations
    - `adverbize()` represents numbers in their numeral adverb representations
    - `truncate()` truncates long sentences at a given limit and append a suffix if needed
    - `singularize()` returns the singular form of a given word
    - `pluralize()` returns the plural form of a given word
- Added the `iterating/` module, containing several helpers for iterables:
    - `renumerate()` enumerates an iterable starting from its end
    - `chunks()` splits an iterable into smaller chunks, padding them if requested
    - `partition()` splits an iterable into the items that validated the given predicate and the others
    - `uniq()` removes duplicates from an iterable while keeping the items' order
    - `compact()` removes None values from an iterable
    - `flatten()` unpacks nested iterable into the given iterable
- Added the `i16g/` module, to help with locale management:
    - `Locale` dynamically loads localization files from a package path
- Added the `importing/` module, a collection of helpers for dynamic importing:
    - `import_class_from_path()` fetches a class from a package path and returns it
    - `import_module_from_path()` exposes the contents of a module as globals from a package path
- Added the `logging/` module, containing drop-in configurations, and custom handlers for logging:
    - `DEFAULT_CONSOLE_CONFIGURATION` prints logs to stderr with a sensible set of information
    - `DJANGO_CONSOLE_CONFIGURATION` prints logs to stderr with the same formatting as Django's logger
    - `FLASK_CONSOLE_CONFIGURATION` prints logs to stderr with the same formatting as Flask's logger
    - `PYRAMID_CONSOLE_CONFIGURATION` prints logs to stderr with the same formatting as Pyramid's logger
    - `RAILS_CONSOLE_CONFIGURATION` prints logs to stderr with the same formatting as Ruby-on-Rails' logger
    - `AffixedStreamHandler` allows custom prefix/suffix to customize the way log records are emitted
    - `@muted` silences all (or selected) loggers during a callable's execution
- Added `Borg` exposes a class useful to produce a singleton behaviour across multiple instances
- Added `Sentinel` exposes a class that can be used to implement the Sentinel design pattern
- Added `Singleton` exposes a metaclass useful to implement the Singleton design pattern
- Added `@classproperty` combines @classmethod and @property (with support for @attr.setter)
- Added `@deprecated` documents deprecated callables with a explicit message
- Added `@retryable` retries failing executing of a callable
- Added `@sampled` implements sampling strategies to filter calls made to a callable
- Added `@timed` measures and prints the execution time of a callable
- Added `@timeoutable` stops the execution of a callable if its run time is too long
