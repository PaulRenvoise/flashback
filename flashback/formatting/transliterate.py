from unidecode import unidecode


def transliterate(text: str, keep_case: bool = True) -> str:
    """
    Replaces unicode characters with their ASCII equivalent using unidecode
    (https://pypi.org/project/Unidecode/).

    Examples:
        ```python
        from flashback.formatting import transliterate

        transliterate("réseau")
        #=> "reseau"

        transliterate("omrežje")
        #=> omrezje

        transliterate("Omrežje", keep_case=True)
        #=> Omrezje
        ```

    Params:
        text: the text to transform from unicode to ASCII
        keep_case: whether or not to keep the input case

    Returns:
        the text using only ASCII characters
    """
    text = str(text)
    text = unidecode(text)

    if keep_case:
        return text

    return text.lower()
