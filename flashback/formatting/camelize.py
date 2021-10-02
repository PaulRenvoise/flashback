import regex

from .snakeize import snakeize


CRE_CAMELIZE = regex.compile(r"(?<!(?:^|-|_))[\-_](?![\-_])(.)", flags=regex.I)

def camelize(text, acronyms=None):
    """
    Transforms a text in any case to camelCase.

    Any character following a matched acronym will be capitalized.

    Examples:
        ```python
        from flashback.formatting import camelize

        camelize("host")
        #=> "host"

        camelize("http_host")
        #=> "httpHost"

        camelize("__http_host__")
        #=> __httpHost__

        camelize("HTTPHost")
        #=> httphOst

        camelize("HTTPHost", acronyms=["HTTP"])
        #=> HTTPHost
        ```

    Params:
        text (str): the text to transform into camelCase
        acronyms (Iterable): a list of correctly cased acronyms to retain and case correctly

    Returns:
        str: the camel cased text
    """
    text = snakeize(text, acronyms=acronyms)

    # Builds the pattern to handle acronyms
    if acronyms is None:
        lower2upper = {}
        acronyms_pattern = r"(?=$)^"
    else:
        lower2upper = {acronym.lower(): acronym for acronym in acronyms}
        acronyms_pattern = "|".join(sorted(acronyms, key=len, reverse=True))

    acronyms_camelize_pattern = fr"({acronyms_pattern})(.|$)"

    text = CRE_CAMELIZE.sub(lambda m: m.group()[1:].upper(), text)

    def replace(m):
        return lower2upper[m.group(1).lower()] + m.group(2).upper()

    text = regex.sub(acronyms_camelize_pattern, replace, text, flags=regex.I)

    return text
