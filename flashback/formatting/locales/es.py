"""
Defines the Spanish localization file for `flashback.formatting.singularize` and
`flashback.formatting.pluralize`.

Inspired by:

- https://github.com/clips/pattern/blob/master/pattern/text/es/inflect.py
"""

import regex


# Prepositions are used in compound words
PREPOSITIONS = set((
    "antes", "durante", "de", "para",
    "en", "detrás", "delante", "adelante",
    "través", "arriba", "bajo", "abajo",
    "después", "dentro", "adentro", "fuera", "afuera", "cerca",
    "entre", "además", "excepto", "alrededor",
    "encima", "debajo", "por encima", "por debajo",
    "espalda", "desde", "con", "sin", "como",
    "hasta", "listo", "vía",
    "por"
))

PLURAL_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^un$", "unos", None),
        (r"^una$", "unas", None),
        (r"^el$", "los", None),
        (r"^la$", "las", None),
        (r"^(est[oae])$", r"\1s", None),
        (r"^(es[oae])$", r"\1s", None),
        (r"^(algun[oa])$", r"\1s", None),
    ),
    # Possessive adjectives
    (
    ),
    # Possessive pronouns
    (
        (r"^(mí(s|[oa]))$", r"\1s", None),
        (r"^(tu(s|y[oa]))$", r"\1s", None),
        (r"^(su(s|y[oa]))$", r"\1s", None),
        (r"^(nuestr[oa])$", r"\1s", None),
        (r"^(vuestr[oa])$", r"\1s", None),
    ),
    # Personal pronouns
    (
        (r"^yo$", "nosotros", None),
        (r"^tú$", "vosotros", None),
        (r"^usted$", "ustedes", None),
        (r"^él$", "ellos", None),
        (r"^ello$", "ellos", None),
        (r"^ella$", "ellas", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
        (r"(idad|esis|isis|osis|dica|grafía|logía)$", r"\1", None),
        (r"(..(a|e|i|o|u)s)$", r"\1", None),
    ),
    # Irregular plural forms
    (
        (r"^(mam|pap)á$", r"\1ás", None),
        (r"^sofá$", "sofás", None),
        (r"dominó$", "dominós", None),
        (r"án$", "anes", None),
        (r"én$", "enes", None),
        (r"ín$", "ines", None),
        (r"ón$", "ones", None),
        (r"ún$", "unes", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"(a|e|i|o|u|é)$", r"\1s", None),
        (r"(á|é|í|ó|ú)$", r"\1es", None),
        (r"és$", "eses", None),
        (r"z$", "ces", None),
    ),
    # Assume that the plural takes -es
    (
        (r"$", "es", None),
    )
]

# For performance, compile the regular expressions once:
PLURAL_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in PLURAL_RULES]

# Suffix categories
PLURAL_CATEGORIES = {
    "uninflected": set((
    )),
    "uncountable": set((
        "poesía", "vino", "café", "harina", "detergente",
        "pimienta", "leche", "ketchup", "sangre", "política",
    )),
    "nationalities": set((
    )),
}


SINGULAR_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^unos$", "un", None),
        (r"^unas$", "una", None),
        (r"^los$", "el", None),
        (r"^las$", "la", None),
        (r"^(est[oae])s$", r"\1", None),
        (r"^(es[oae])s$", r"\1", None),
        (r"^(algun[oa])s$", r"\1", None),
    ),
    # Possessive adjectives
    (
    ),
    # Possessive pronouns
    (
        (r"^(mí(s|[oa]))s$", r"\1", None),
        (r"^(tu(s|y[oa]))s$", r"\1", None),
        (r"^(su(s|y[oa]))s$", r"\1", None),
        (r"^(nuestr[oa])s$", r"\1", None),
        (r"^(vuestr[oa])s$", r"\1", None),
    ),
    # Personal pronouns
    (
        (r"^nosotros$", "yo", None),
        (r"^vosotros$", "tú", None),
        (r"^ustedes$", "usted", None),
        (r"^ellos$", "él", None),
        (r"^ellas$", "ella", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
    ),
    # Irregular plural forms
    (
        (r"^(mam|pap)ás$", r"\1á", None),
        (r"^sofás$", "sofá", None),
        (r"dominós$", "dominó", None),
        (r"anes$", "án", None),
        (r"enes$", "én", None),
        (r"ines$", "ín", None),
        (r"ones$", "ón", None),
        (r"unes$", "ún", None),
        (r"eses$", "és", None),
        (r"(br|i|j|t|zn)es$", r"\1e", None),
        (r"(esis|isis|osis)$", r"\1", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"ces$", "z", None),
    ),
    # Assume that the plural takes -es
    (
        (r"es$", "", None),
        (r"s$", "", None),
    )
]

# For performance, compile the regular expressions once:
SINGULAR_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in SINGULAR_RULES]

# Suffix categories
SINGULAR_CATEGORIES = {
    "uninflected": set((
    )),
    "uncountable": set((
    )),
    "nationalities": set((
    ))
}
