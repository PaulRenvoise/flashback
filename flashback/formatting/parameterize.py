import regex

from .transliterate import transliterate


CRE_PARAMETERIZE_NON_ALPHANUM = regex.compile(r"[^a-z0-9\-_]+", flags=regex.I)  # pylint: disable=no-member

def parameterize(text, sep="-", keep_case=False):
    """
    Replaces special characters in a text so that it may be used as part of an URL.

    Internally, uses `flashback.formatting.transliterate` to replace any unicode
    character by its ASCII equivalent.

    Examples:
        ```python
        from flashback.formatting import parameterize

        parameterize("Host")
        #=> "host"

        parameterize("HTTPHost")
        #=> "httphost"

        parameterize("HTTP Host")
        #=> "http-host"

        parameterize("Redis Server", sep="/")
        #=> "redis/server"
        ```

    Params:
        text (str): the text to transform
        sep (str): the separator to use as replacement
        keep_case (bool): whether or not to keep the input case

    Returns:
        str: the parameterized text
    """
    text = transliterate(text)

    # Turn unwanted chars into a separator
    text = CRE_PARAMETERIZE_NON_ALPHANUM.sub(sep, text)

    if sep:
        sep = regex.escape(sep)

        # No more than one separator in a row
        text = regex.sub(rf"{sep}{{2,}}", sep, text)

        # Remove leading and trailing separators
        text = regex.sub(rf"^{sep}|{sep}$", "", text)

    if keep_case:
        return text

    return text.lower()
