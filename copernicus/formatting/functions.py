import regex

from unidecode import unidecode


CRE_CAMELIZE_FIRST_CHAR = regex.compile(r"(?:^|_)(.)", flags=regex.I)

CRE_SNAKEIZE_CAPITAL_WORDS = regex.compile(r"([A-Z\d]+)([A-Z][a-z])")
CRE_SNAKEIZE_LOWER_WORDS = regex.compile(r"([a-z\d])([A-Z])")
CRE_SNAKEIZE_MULTI_UNDERSCORES = regex.compile(r"_{2,}")
CRE_SNAKEIZE_STRIP_UNDERSCORES = regex.compile(r"^_|_$")

CRE_PARAMETERIZE_NON_ALPHANUM = regex.compile(r"[^a-z0-9\-_]+", flags=regex.I)


def oxford_join(iterable, sep=', ', couple_sep=' and ', last_sep=', and ', quotes=False):
    """
    Joins a list of string to a comma-separated sentence in a more english fashion than the builtin `.join()`.

    Args:
        - iterable (Iterable) : the sequence holding the strings to join
        - sep (str) : the separator used when there is more than two items in `interable`
        - couple_sep (str) : the separator to use if there is only two items in `iterable`
        - last_sep (str) : the separator to use for the last two items of `iterable`

    Returns:
        - str : the joined strings
    """
    if len(iterable) == 0:
        return ''

    if quotes:
        iterable = [f"'{item}'" for item in iterable]
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

    Args:
        - text (str) : the text to transform from unicode to ASCII
        - keep_case (bool) : whether or not to keep the input case

    Returns:
        - str : the text using only ASCII characters
    """
    text = str(text)
    text = unidecode(text)

    if keep_case:
        return text

    return text.lower()


def camelize(text, acronyms=None):
    """
    Transforms a any-cased text to CamelCase.

    Any character following a matched acronym will be capitalized.

    Args:
        - text (str) : the text to transform into CamelCase
        - acronyms (Iterable) : a list of correctly cased acronyms to retain and case correctly

    Returns:
        - str : the camel cased text
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

    Args:
        - text (str) : the text to transform into snake_case
        - acronyms (Iterable) : a list of acronyms to treat as non-delimited single lowercase words

    Returns:
        - str : the snake cased text
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

    Uses `copernicus.formatting.functions.transliterate` to replace unicode characters by their ASCII equivalent.

    Args:
        - text (str) : the text to transform
        - sep (str) : the separator to use as replacement
        - keep_case (bool) : whether or not to keep the input case

    Returns:
        - str : the parameterized text
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

    Args:
        - number (int) : the number to transform to an ordinal number

    Returns:
        - str : the number with the correct ordinal suffix
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

    For reference about numeral adverbs, see: http://tiny.cc/m4bkez

    Args:
        - number (int) : the number for transform to a numeral adverb

    Returns:
        - str : the numeral adverb
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
