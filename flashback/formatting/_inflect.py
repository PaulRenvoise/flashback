from __future__ import annotations

from collections.abc import Callable

import regex


CRE_INFLECT_ONLY_PUNCT_SYM_NUM = regex.compile(r"^[\p{P}\p{S}\p{N}]+$", flags=regex.U)


def _inflect(
    word: str,
    rules: list[tuple[str, str, str | None]],
    categories: dict[str, set[str]],
    prepositions: set[str],
    base_case: Callable[[str], str] = str.lower,
) -> str:
    word = base_case(str(word))

    if CRE_INFLECT_ONLY_PUNCT_SYM_NUM.search(word):
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
