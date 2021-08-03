from ..i16g import Locale
from ._inflect import _inflect


def singularize(word, language="en"):
    """
    Returns the singular form of the given word.

    Examples:
        ```python
        from flashback.formatting import singularize

        singularize("networks")
        #=> "network"

        singularize("databases-as-a-service")
        #=> "database-as-a-service"

        singularize("réseaux", language="fr")
        #=> "réseau"
        ```

    Params:
        word (str): the word to singularize
        language (str): the language to use to singularize the word (ISO 639-1)

    Returns:
        str: the singularized word
    """
    locale = Locale.load(language, path=".locales")

    # TODO: find a way to put that in _inflect
    if language == "en":
        if word.endswith(("'", "'s")):
            sub_word = word.rstrip("s")
            sub_word = sub_word.rstrip("'")
            sub_word = singularize(sub_word)

            if sub_word.endswith("s"):
                return f"{sub_word}'"

            return f"{sub_word}'s"

    base_case = str.lower if language != "de" else str.capitalize

    return _inflect(word, locale.SINGULAR_RULES, locale.SINGULAR_CATEGORIES, locale.PREPOSITIONS, base_case=base_case)
