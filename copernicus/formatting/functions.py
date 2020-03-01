import regex


CRE_CAMELIZE_FIRST_CHAR = regex.compile(r"(?:^|_)(.)", flags=regex.I)

CRE_SNAKEIZE_CAPITAL_WORDS = regex.compile(r"([A-Z\d]+)([A-Z][a-z])")
CRE_SNAKEIZE_LOWER_WORDS = regex.compile(r"([a-z\d])([A-Z])")
CRE_SNAKEIZE_MULTI_UNDERSCORES = regex.compile(r"_{2,}")
CRE_SNAKEIZE_STRIP_UNDERSCORES = regex.compile(r"^_|_$")


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
