from ..i16g import Locale
from ._inflect import _inflect


def pluralize(word, language="en"):
    """
    Returns the plural form of the given word.

    Examples:
        ```python
        from flashback.formatting import pluralize

        pluralize("network")
        #=> "networks"

        pluralize("database-as-a-service")
        #=> "databases-as-a-service"

        pluralize("réseau", language="fr")
        #=> "réseaux"
        ```

    Params:
        word (str): the word to pluralize
        language (str): the language to use to pluralize the word (ISO 639-1)

    Returns:
        str: the pluralized word
    """
    locale = Locale.load(language, path=".locales")

    # TODO: find a way to put that in _inflect
    if language == "en":
        if word.endswith(("'", "'s")):
            sub_word = word.rstrip("s")
            sub_word = sub_word.rstrip("'")
            sub_word = pluralize(sub_word)

            if sub_word.endswith("s"):
                return f"{sub_word}'"

            return f"{sub_word}'s"

    base_case = str.lower if language != "de" else str.capitalize

    return _inflect(word, locale.PLURAL_RULES, locale.PLURAL_CATEGORIES, locale.PREPOSITIONS, base_case=base_case)
