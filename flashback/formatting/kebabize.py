from __future__ import annotations

from collections.abc import Iterable

import regex

from .snakeize import snakeize


CRE_KEBABIZE_UNDERSCORES = regex.compile(r"(?<!(?:^|_))_(?!(?:_|$))")


def kebabize(text: str, acronyms: Iterable[str] | None = None) -> str:
    """
    Transforms a text in any case to kebab-case.

    Does not mutilate protected names (names prefixed with '_') and dunder_names (names surrounded
    by '__').

    Examples:
        ```python
        from flashback.formatting import kebabize

        kebabize("host")
        #=> "host"

        kebabize("httpHost")
        #=> "http-host"

        kebabize("__http_host__")
        #=> "__http-host__"

        kebabize("HTTPHost")
        #=> "httph-ost"

        kebabize("HTTPHost", acronyms=["HTTP"])
        #=>"http-host"
        ```

    Params:
        text: the text to transform into kebab-case
        acronyms: a list of acronyms to treat as non-delimited single lowercase words

    Returns:
        the kebab cased text
    """
    return CRE_KEBABIZE_UNDERSCORES.sub("-", snakeize(text, acronyms=acronyms))
