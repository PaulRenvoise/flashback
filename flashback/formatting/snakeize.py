import regex


CRE_SNAKEIZE_CAPITAL_WORDS = regex.compile(r"([A-Z\d]+)([A-Z][a-z])")
CRE_SNAKEIZE_LOWER_WORDS = regex.compile(r"([a-z\d])([A-Z])")
CRE_SNAKEIZE_UNDERSCORES = regex.compile(r"(?<!^)_(?=_.)")

def snakeize(text, acronyms=None):
    """
    Transforms a text in any case to snake_case.

    Does not mutilate protected names (names prefixed with '_') and dunder_names (names surrounded
    by '__').

    Examples:
        ```python
        from flashback.formatting import snakeize

        snakeize("host")
        #=> "host"

        snakeize("httpHost")
        #=> "http_host"

        snakeize("__httpHost__")
        #=> "__http_host__"

        snakeize("HTTPHost")
        #=> "httph_ost"

        snakeize("HTTPHost", acronyms=["HTTP"])
        #=> "http_host"
        ```

    Params:
        text (str): the text to transform into snake_case
        acronyms (Iterable): a list of acronyms to treat as non-delimited single lowercase words

    Returns:
        str: the snake cased text
    """
    text = str(text)

    acronyms_pattern = r"(?=$)^" if acronyms is None else "|".join(acronyms)
    acronyms_snakeize_pattern = rf"({acronyms_pattern})"

    for match in regex.finditer(acronyms_snakeize_pattern, text, flags=regex.I):
        parts = []

        start = text[:match.start()]
        if start:
            parts.append(start)

        parts.append(match.group(1))

        end = text[match.end():]
        if end:
            parts.append(end)

        text = "_".join(parts)

    text = CRE_SNAKEIZE_CAPITAL_WORDS.sub(r"\1_\2", text)
    text = CRE_SNAKEIZE_LOWER_WORDS.sub(r"\1_\2", text)
    text = text.replace(r"-", "_")

    # Cleanup the unwanted underscores
    text = CRE_SNAKEIZE_UNDERSCORES.sub("", text)

    return text.lower()
