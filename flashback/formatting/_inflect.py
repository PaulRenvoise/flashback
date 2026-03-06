from collections.abc import Callable

import re
import unicodedata


def _is_only_punctuation_symbol_number(text: str) -> bool:
    return bool(text) and all(unicodedata.category(ch)[0] in {"P", "S", "N"} for ch in text)


def _inflect(
    word: str,
    rules: list[list[tuple[re.Pattern, str, str | None]]],
    categories: dict[str, set[str]],
    prepositions: set[str],
    base_case: Callable[[str], str] = str.lower,
) -> str:
    word = base_case(str(word))

    if _is_only_punctuation_symbol_number(word):
        return word

    # Recurses over compound words like mothers-in-law, eco-friendly, post-nap
    tokens = word.replace("-", " ").split(" ")
    if len(tokens) > 1:
        if tokens[1] in prepositions:
            return word.replace(tokens[0], _inflect(tokens[0], rules, categories, prepositions))

        return word.replace(tokens[-1], _inflect(tokens[-1], rules, categories, prepositions))

    # Applies rules
    for rule in rules:
        for suffix, inflection, category in rule:
            # A general rule
            if category is None:
                if suffix.search(word) is not None:
                    return suffix.sub(inflection, word)
            elif word in categories[category]:
                return suffix.sub(inflection, word)

    # Should never be reached, but just in case
    return word
