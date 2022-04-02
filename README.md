<p align="center">
    <img src="https://raw.githubusercontent.com/PaulRenvoise/flashback/develop/assets/logo.png" alt="Flashback"></a>
</p>
<h3 align="center">Flashback</h3>
<p align="center">You've probably already implemented it.</p>

---

Flashback is a collection of python utilities: it contains classes, metaclasses, decorators,
functions, constants, etc. that you might have written a couple times already.

## Installing

Flashback supports python 3.7+.

Pip:
```bash
pip install flashback
```

Build from sources:
```bash
git clone git@github.com:PaulRenvoise/flashback.git
cd flashback
python setup.py install
```

## Contents

Flashback's helpers are currently organised within 7 modules, and global helpers:

- `accessing/`
    - `dig()` recursively fetch keys in a nested dict
- `caching/`
    - `Cache` supports several cache stores: in-memory, disk, Redis, and Memcached
    - `@cached` caches a callable's return value based on its arguments
- `debugging/`
    - `xp()` prints debug information about its given arguments
    - `@profiled` collects and dumps profiling stats over a callable's execution
    - `caller()` allows a developer to print debug information about a callable's caller
    - `get_callable()` extracts a callable instance from a frame
    - `get_call_context()` finds and returning the code context around a call made in a frame
    - `get_frameinfo()` implements a faster `inspect.stack()[x]`
- `formatting/`
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
- `iterating/`
    - `renumerate()` enumerates an iterable starting from its end
    - `chunks()` splits an iterable into smaller chunks, padding them if requested
    - `partition()` splits an iterable into items validating a predicate and the ones that don't
    - `uniq()` removes duplicates from an iterable while keeping the items' order
    - `compact()` removes None values from an iterable
    - `flatten()` unpacks nested iterable into the given iterable
    - `flat_map()` applies a function to every item and nested item of the given iterable
- `i16g/`
    - `Locale` dynamically loads localization files from a package path
- `importing/`
    - `import_class_from_path()` fetches a class from a package path and returns it
    - `import_module_from_path()` exposes the contents of a module as globals from a package path
- `logging/`
    - `DEFAULT_CONSOLE_CONFIGURATION` logs to stderr with a sensible set of information
    - `DJANGO_CONSOLE_CONFIGURATION` logs to stderr with the same formatting as Django's logger
    - `FLASK_CONSOLE_CONFIGURATION` logs to stderr with the same formatting as Flask's logger
    - `PYRAMID_CONSOLE_CONFIGURATION` logs to stderr with the same formatting as Pyramid's logger
    - `RAILS_CONSOLE_CONFIGURATION` logs to stderr with the same formatting as RoR's logger
    - `AffixedStreamHandler` allows custom affixes to log records
    - `@muted` silences all (or selected) loggers during a callable's execution
- `EncryptedFile` exposes a mechanism to read and write encrypted contents to a file
- `Borg` exposes a class useful to produce a singleton behaviour across multiple instances
- `Sentinel` exposes a class that can be used to implement the Sentinel design pattern
- `Singleton` exposes a metaclass useful to implement the Singleton design pattern
- `@classproperty` combines @classmethod and @property (with support for @attr.setter)
- `@deprecated` documents deprecated callables with a explicit message
- `@retryable` retries failing executing of a callable
- `@sampled` implements sampling strategies to filter calls made to a callable
- `@timed` measures and prints the execution time of a callable
- `@timeoutable` stops the execution of a callable if its run time is too long

## Contributing

The Pull Request template has a checklist containing everything you need to submit a new PR.

Run the tests with `pytest`:
```bash
pytest tests
```

Run the lint with `pylint`:
```bash
pylint flashback/ tests/
```

## License

Flashback is released under the [MIT License](https://tldrlegal.com/license/mit-license#summary).
