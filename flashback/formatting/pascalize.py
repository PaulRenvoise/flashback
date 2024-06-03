from __future__ import annotations

from collections.abc import Iterable

import regex

from .camelize import camelize


CRE_PASCALIZE = regex.compile(r"^(?:_{1,2}|)([a-z\d])(?:[a-z\d]+)")


def pascalize(text: str, acronyms: Iterable[str] | None = None) -> str:
    """
    Transforms a text in any case to PascalCase.

    Any character following a matched acronym will be capitalized.

    Examples:
        ```python
        from flashback.formatting import pascalize

        pascalize("host")
        #=> "Host"

        pascalize("http_host")
        #=> "HttpHost"

        pascalize("__http_host__")
        #=> "__HttpHost__"

        pascalize("HTTPHost")
        #=> "HttphOst"

        pascalize("HTTPHost", acronyms=["HTTP"])
        #=> "HTTPHost"
        ```

    Params:
        text: the text to transform into PascalCase
        acronyms: a list of correctly cased acronyms to retain and case correctly

    Returns:
        the pascal cased text
    """
    text = camelize(text, acronyms=acronyms)

    def replace(m: regex.Match) -> str:
        group = m.group()

        if "_" in group:
            underscore_index = group.rindex("_") + 1
            return group[:underscore_index] + group[underscore_index:].capitalize()

        return group.capitalize()

    return CRE_PASCALIZE.sub(replace, text)
