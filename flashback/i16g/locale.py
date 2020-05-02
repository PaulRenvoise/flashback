import inspect

from importlib import util, import_module

import regex


class Locale:
    """
    Defines a generic loader that finds, imports, caches, and returns constants used for internationalization.

    Examples:
        ```python
        TODO
        ```
    """
    __cache = {}
    CRE_LOCALE = regex.compile(r"""
            ^
            (?P<language>
                [a-z]{2}
            )
            (?:
                [-_]
                (?P<territory>
                    [a-z]{2}
                )
                (?:
                    [\.:]
                    (?P<codeset>
                        .+
                    )?
                    (?:
                        @
                        (?P<modifier>
                            .+
                        )
                    )
                )?
            )?
        """, regex.I + regex.X)

    @classmethod
    def load(cls, locale, path):
        """
        Loads a locale definition from a relative or absolute path and expose its contents.
        If the path is relative, it is transformed to absolute using the call stack and the given relative path.

        This method generates locales candidates to use as fallback, e.g.: 'en_US.UTF-8' will yield 'en_us' and 'en'.
        We'll then try go from the most to the least precise ('en_us', then 'en') until we import something.

        The cache uses the complete localization file's path to avoid conflicts and overrides.

        The code is very similar to `flashback.importing.functions.import_module_from_path` with the following tweaks:
            - We have several candidates that can be imported
            - We cache the imported module

        Examples:
            ```python
            from flashback.i16g import Locale

            Locale.load('fr_FR', '.languages')
            #=> Whatever defined in fr_FR

            Locale.load('fr_FR.UTF-8@latin', 'config.locales')
            #=> Whatever defined in fr_FR

            Locale.load('not-implemented', 'conf.production')
            #=> NotImplementedError
            ```

        Params:
            - `locale (str)` the given locale
            - `path (str)` the path in which to find the locale definition

        Returns:
            - `Module` the content of the loaded locale

        Raises:
            - `NotImplementedError` if the given locale implementation is not found
        """
        locale = cls.simplify(locale)

        candidate_locales = sorted({locale, locale.split('_')[0]}, key=len, reverse=True)

        if path.startswith('.'):
            caller_module = inspect.getmodule(inspect.stack()[1][0])
            caller_package = caller_module.__package__

            module_path = util.resolve_name(path, caller_package)
        else:
            module_path = path

        for candidate_locale in candidate_locales:
            locale_full_path = module_path + '.' + candidate_locale

            if locale_full_path in cls.__cache:
                return cls.__cache[locale_full_path]

            # Loads the module, will suppress ImportError if module cannot be loaded
            # because we will raise NotImplementedError only once we've been through all locale candidates
            try:
                imported_locale = import_module(locale_full_path)

                cls.__cache[locale_full_path] = imported_locale

                return imported_locale
            except ImportError:
                pass

        raise NotImplementedError(f"Locale {locale!r} is not implemented in {module_path}.")

    @classmethod
    def simplify(cls, locale):
        """
        Returns a simplified locale code for the given locale name.

        The returned locale code is formatted as `LANGUAGE_TERRITORY` (e.g. 'en_US.UTF-8' to 'en_us'),
        or `LANGUAGE` (e.g. 'EN' to 'en') if the territory was not specified in the given locale.

        If normalization fails, the original name is returned unchanged.

        Examples:
            ```python
            from flashback.i16g import Locale

            Locale.simplify('uz_UZ.UTF-8@cyrillic')
            #=> uz_UZ

            Locale.simplify('en@latin-1')
            #=> 'en'

            Locale.simplify('fr.ISO-8859-1@latin')
            #=> 'fr'

            Locale.simplify('not-a-locale')
            #=> 'not-a-locale'
            ```

        Params:
            - `locale (str)` the non-normalized locale string

        Returns:
            - `str` the lowercased locale containing at least the language (and if given, the territory)
        """
        match = cls.CRE_LOCALE.match(locale)
        if not match:
            return locale

        # If we have a match, we necessarily have a language
        simplified_locale = match.group('language').lower()

        territory = match.group('territory')
        if territory:
            simplified_locale = simplified_locale + "_" + territory.lower()

        return simplified_locale
