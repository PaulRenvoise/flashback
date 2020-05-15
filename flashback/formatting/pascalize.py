import regex

from .camelize import camelize


CRE_PASCALIZE = regex.compile(r"^(?:_{1,2}|)([a-z\d])(?:[a-z\d]+)")

def pascalize(text, acronyms=None):
    """
    Transforms a text in any case to PascalCase.

    Any character following a matched acronym will be capitalized.

    Examples:
        ```python
        from flashback.formatting import pascalize

        assert pascalize('host') == 'Host'
        assert pascalize('http_host') == 'HttpHost'
        assert pascalize('__http_host__') == '__HttpHost__'
        assert pascalize('HTTPHost') == 'HttphOst'
        assert pascalize('HTTPHost', acronyms=['HTTP']) == 'HTTPHost'
        ```

    Params:
        - `text (str)` the text to transform into PascalCase
        - `acronyms (Iterable)` a list of correctly cased acronyms to retain and case correctly

    Returns:
        - `str` the pascal cased text
    """
    text = camelize(text, acronyms=acronyms)

    def replace(m):
        group = m.group()

        if '_' in group:
            underscore_index = group.rindex('_') + 1
            return group[:underscore_index] + group[underscore_index:].capitalize()

        return group.capitalize()

    return CRE_PASCALIZE.sub(replace, text)
