# pylint: disable=too-many-lines

import regex

from unidecode import unidecode

from ..i16g import Locale


CRE_CAMELIZE_FIRST_CHAR = regex.compile(r"(?:^|_)(.)", flags=regex.I)

CRE_SNAKEIZE_CAPITAL_WORDS = regex.compile(r"([A-Z\d]+)([A-Z][a-z])")
CRE_SNAKEIZE_LOWER_WORDS = regex.compile(r"([a-z\d])([A-Z])")
CRE_SNAKEIZE_MULTI_UNDERSCORES = regex.compile(r"_{2,}")
CRE_SNAKEIZE_STRIP_UNDERSCORES = regex.compile(r"^_|_$")

CRE_PARAMETERIZE_NON_ALPHANUM = regex.compile(r"[^a-z0-9\-_]+", flags=regex.I)

CRE_INFLECT_ONLY_PUNCT_SYM_NUM = regex.compile(r"^[\p{P}\p{S}\p{N}]+$", flags=regex.U)


def oxford_join(iterable, sep=', ', couple_sep=' and ', last_sep=', and ', quotes=False):
    """
    Joins a list of string to a comma-separated sentence in a more english fashion than the builtin `.join()`.

    Examples:
        ```python
        from flashback.formatting import oxford_join

        oxford_join('A', 'B')
        #=> "A and B"

        oxford_join('A', 'B', 'C')
        #=> "A, B, and C"

        oxford_join('A', 'B', 'C', last_sep=', or ')
        #=> "A, B, or C"
        ```

    Params:
        - `iterable (Iterable<Any>)` the sequence holding the items to join
        - `sep (str)` the separator used when there is more than two items in the iterable
        - `couple_sep (str)` the separator to use if there is only two items in the iterable
        - `last_sep (str)` the separator to use for the last two items of the iterable
        - `quotes (bool)` whether or not to add quotes around each item of the iterable

    Returns:
        - `str` the joined strings
    """
    if len(iterable) == 0:
        return ''

    if quotes:
        iterable = [f"\"{item}\"" for item in iterable]
    else:
        iterable = [str(item) for item in iterable]

    if len(iterable) == 1:
        return iterable[0]

    if len(iterable) == 2:
        return couple_sep.join(iterable)

    enumeration = sep.join(iterable[:-1])

    return f"{enumeration}{last_sep}{iterable[-1]}"


def transliterate(text, keep_case=True):
    """
    Replaces unicode characters with their ASCII equivalent using unidecode (https://pypi.org/project/Unidecode/).

    Examples:
        ```python
        from flashback.formatting import transliterate

        transliterate('réseau')
        #=> "reseau"

        transliterate('omrežje')
        #=> omrezje

        transliterate('Omrežje', keep_case=True)
        #=> Omrezje
        ```

    Params:
        - `text (str)` the text to transform from unicode to ASCII
        - `keep_case (bool)` whether or not to keep the input case

    Returns:
        - `str` the text using only ASCII characters
    """
    text = str(text)
    text = unidecode(text)

    if keep_case:
        return text

    return text.lower()


def camelize(text, acronyms=None):
    """
    Transforms a any-cased text to CamelCase. Any character following a matched acronym will be capitalized.

    Examples:
        ```python
        from flashback.formatting import camelize

        camelize('host')
        #=> "Host"

        camelize('http_host')
        #=> "HttpHost"

        camelize('http_host', acronyms=['HTTP'])
        #=> HTTPHost
        ```

    Params:
        - `text (str)` the text to transform into CamelCase
        - `acronyms (Iterable)` a list of correctly cased acronyms to retain and case correctly

    Returns:
        - `str` the camel cased text
    """
    text = str(text)

    # Build the pattern to handle acronyms
    if acronyms is None:
        lower2upper = {}
        acronyms_pattern = r"(?=$)^"
    else:
        lower2upper = {acronym.lower(): acronym for acronym in acronyms}
        acronyms_pattern = '|'.join(sorted(acronyms, key=len, reverse=True))

    acronyms_camelize_pattern = r"({})(.|$)".format(acronyms_pattern)

    # Capitalize
    text = CRE_CAMELIZE_FIRST_CHAR.sub(lambda x: x.group(1).capitalize(), text)

    # Iterate on all acronyms matches then:
    # Use the given casing, and uppercase the following char
    for match in regex.finditer(acronyms_camelize_pattern, text, flags=regex.I):
        replacement = lower2upper[match.group(1).lower()] + match.group(2).capitalize()
        text = text[:match.start()] + replacement + text[match.end():]

    return text


def snakeize(text, acronyms=None):
    """
    Transforms an any-cased text to snake_case.

    Examples:
        ```python
        from flashback.formatting import snakeize

        snakeize('host')
        #=> "host"

        snakeize('HTTPHost')
        #=> "httph_ost"

        snakeize('HTTPHost', acronyms=['HTTP'])
        #=> 'http_host'
        ```

    Params:
        - `text (str)` the text to transform into snake_case
        - `acronyms (Iterable)` a list of acronyms to treat as non-delimited single lowercase words

    Returns:
        - `str` the snake cased text
    """
    text = str(text)

    acronyms_pattern = r"(?=$)^" if acronyms is None else '|'.join(acronyms)
    acronyms_underscorize_pattern = r"({})".format(acronyms_pattern)

    for match in regex.finditer(acronyms_underscorize_pattern, text, flags=regex.I):
        text = '_'.join([text[:match.start()], match.group(1), text[match.end():]])

    text = CRE_SNAKEIZE_CAPITAL_WORDS.sub(r"\1_\2", text)
    text = CRE_SNAKEIZE_LOWER_WORDS.sub(r"\1_\2", text)
    text = text.replace(r"-", '_')

    # Cleanup the unwanted underscores
    text = CRE_SNAKEIZE_MULTI_UNDERSCORES.sub('_', text)
    text = CRE_SNAKEIZE_STRIP_UNDERSCORES.sub('', text)

    return text.lower()


def parameterize(text, sep='-', keep_case=False):
    """
    Replaces special characters in a text so that it may be used as part of an URL.

    Internally, uses `flashback.formatting.functions.transliterate` to replace any unicode character found
    by its ASCII equivalent.

    Examples:
        ```python
        from flashback.formatting import parameterize

        parameterize('Host')
        #=> "host"

        parameterize('HTTPHost')
        #=> "httphost"

        parameterize('HTTP Host')
        #=> "http-host"

        parameterize('Redis Server', sep='/')
        #=> "redis/server"
        ```

    Params:
        - `text (str)` the text to transform
        - `sep (str)` the separator to use as replacement
        - `keep_case (bool)` whether or not to keep the input case

    Returns:
        - `str` the parameterized text
    """
    text = transliterate(text)

    # Turn unwanted chars into a separator
    text = CRE_PARAMETERIZE_NON_ALPHANUM.sub(sep, text)

    if sep:
        sep = regex.escape(sep)

        # No more than one separator in a row
        text = regex.sub(r"{}{{2,}}".format(sep), sep, text)

        # Remove leading and trailing separators
        text = regex.sub(r"^{sep}|{sep}$".format(sep=sep), '', text)

    if keep_case:
        return text

    return text.lower()


def ordinalize(number):
    """
    Transforms a number to its ordinal representation.
    Since this method should be mostly used in logging messages, only English is supported.

    Examples:
        ```python
        from flashback.formatting import ordinalize

        ordinalize(1)
        #=>  "1st"

        ordinalize(3)
        #=> "3rd"

        ordinalize(144)
        #=> "144th"
        ```

    Params:
        - `number (int)` the number to transform to an ordinal number

    Returns:
        - `str` the number with the correct ordinal suffix
    """
    number = int(number)

    if number == 1:
        suffix = 'st'
    elif number == 2:
        suffix = 'nd'
    elif number == 3:
        suffix = 'rd'
    elif number in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        suffix = 'th'
    else:
        modulo = abs(number) % 100
        if modulo > 13:
            modulo %= 10

        if modulo == 1:
            suffix = 'st'
        elif modulo == 2:
            suffix = 'nd'
        elif modulo == 3:
            suffix = 'rd'
        else:
            suffix = 'th'

    return f"{number}{suffix}"


def adverbize(number):
    """
    Transforms a number to its numeral adverb representation.
    Since this method should be mostly used in logging messages, only English is supported.

    For reference about numeral adverbs, see: http://tiny.cc/m4bkez.

    Examples:
        ```python
        from flashback.formatting import adverbize

        adverbize(1)
        #=> "once"

        adverbize(3)
        #=> "thrice"

        adverbize(144)
        #=> "144 times"
        ```

    Params:
        - `number (int)` the number for transform to a numeral adverb

    Returns:
        - `str` the numeral adverb
    """
    number = int(number)

    if number == 1:
        numeral = 'once'
    elif number == 2:
        numeral = 'twice'
    elif number == 3:
        numeral = 'thrice'
    else:
        numeral = f"{number} times"

    return numeral

def truncate(text, limit=120, suffix='...'):
    """
    Truncates the given text up to `limit` and fill its ending with `suffix`.

    Tries to find the latest space before the `limit` which is located in the
    second half of the text. If no space is found, truncate at the limit.

    Searching for a space in the second-half of the text avoids cases where
    the word going over the limit is very long, e.g.:

    Without:
    ```python
    truncate("I spectrophotofluorometrically assessed this sample", limit=25)
    #=> 'I...'
    ```
    With:
    ```python
    truncate("I spectrophotofluorometrically assessed this sample", limit=25)
    #=> 'I spectrophotofluorom...'
    ```

    Adapted from https://github.com/reddit/reddit/blob/master/r2/r2/lib/utils/utils.py#L407.

    Examples
        ```python
        from flashback.formatting import truncate

        truncate('This helper is very useful for preview of descriptions', limit=50)
        #=> 'This helper is very useful for preview of...'

        truncate('Wonderful tool to use in any projects!', limit=35, suffix=', bla bla bla')
        #=> 'Wonderful tool to use, bla bla bla'

        truncate('Hi there', limit=3, suffix='')
        #=> 'Hi'
        ```

    Params:
        - `text (str)`
        - `limit (int)`
        - `suffix(str)`

    Returns
        - `str` the truncated text
    """
    if len(text) <= limit:
        return text

    truncated_text = text[:(limit - len(suffix))]
    try:
        space_index = truncated_text.rindex(' ')
    except ValueError:
        space_index = -1

    if space_index < limit // 2:
        space_index = -1

    return truncated_text[:space_index] + suffix


def singularize(word, language='en'):
    """
    Returns the singular form of the given word.

    Examples:
        ```python
        from flashback.formatting import singularize

        singularize('networks')
        #=> "network"

        singularize('databases-as-a-service')
        #=> "database-as-a-service"

        singularize('réseaux', language='fr')
        #=> "réseau"
        ```

    Params:
        - `word (str)` the word to singularize
        - `language (str)` the language to use to singularize the word (ISO 639-1)

    Returns:
        - `str` the singularized word
    """
    locale = Locale.load(language, path='.locales')

    # TODO: find a way to put that in _inflect
    if language == 'en':
        if word.endswith(("'", "'s")):
            sub_word = word.rstrip("s")
            sub_word = sub_word.rstrip("'")
            sub_word = singularize(sub_word)

            if sub_word.endswith('s'):
                return f"{sub_word}'"

            return f"{sub_word}'s"

    base_case = str.lower if language != 'de' else str.capitalize

    return _inflect(word, locale.SINGULAR_RULES, locale.SINGULAR_CATEGORIES, locale.PREPOSITIONS, base_case=base_case)


def pluralize(word, language='en'):
    """
    Returns the plural form of the given word.

    Examples:
        ```python
        from flashback.formatting import pluralize

        pluralize('network')
        #=> "networks"

        pluralize('database-as-a-service')
        #=> "databases-as-a-service"

        pluralize('réseau', language='fr')
        #=> "réseaux"
        ```

    Params:
        - `word (str)` the word to pluralize
        - `language (str)` the language to use to pluralize the word (ISO 639-1)

    Returns:
        - `str` the pluralized word
    """
    locale = Locale.load(language, path='.locales')

    # TODO: find a way to put that in _inflect
    if language == 'en':
        if word.endswith(("'", "'s")):
            sub_word = word.rstrip("s")
            sub_word = sub_word.rstrip("'")
            sub_word = pluralize(sub_word)

            if sub_word.endswith('s'):
                return f"{sub_word}'"

            return f"{sub_word}'s"

    base_case = str.lower if language != 'de' else str.capitalize

    return _inflect(word, locale.PLURAL_RULES, locale.PLURAL_CATEGORIES, locale.PREPOSITIONS, base_case=base_case)


def _inflect(word, rules, categories, prepositions, base_case=str.lower):
    word = base_case(str(word))

    if CRE_INFLECT_ONLY_PUNCT_SYM_NUM.search(word):
        return word

    # Recurse compound words like mothers-in-law, eco-friendly, post-nap
    tokens = word.replace('-', ' ').split(' ')
    if len(tokens) > 1:
        if tokens[1] in prepositions:
            return word.replace(tokens[0], _inflect(tokens[0], rules, categories, prepositions))

        return word.replace(tokens[-1], _inflect(tokens[-1], rules, categories, prepositions))

    # Apply rules
    for rule in rules:
        for suffix, inflection, category in rule:
            # A general rule
            if category is None:
                if suffix.search(word) is not None:
                    return suffix.sub(inflection, word)

            # A rule pertaining to a specific category of words
            if category is not None:
                if word in categories[category]:
                    return suffix.sub(inflection, word)

    # Should never be reached, but just in case
    return word
