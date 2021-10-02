"""
Defines the German localization file for `flashback.formatting.singularize` and
`flashback.formatting.pluralize`.

Inspired by:

- https://github.com/clips/pattern/blob/master/pattern/text/de/inflect.py
"""

import regex


# Prepositions are used in compound words
PREPOSITIONS = set((
    "vor", "während", "bis zu",
    "über", "hinter", "außer", "als", "aus", "zu",
    "gegenüber", "unten", "für", "auf", "unter",
    "nach", "unterhalb", "von", "onto", "bis",
    "neben", "in", "bis",
    "um", "besides", "über",
    "at", "zwischen", "nahe", "seit", "mit", "ohne",
    "quer", "dwars",
    "jenseits", "aber", "sondern", "bei"
))

PLURAL_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^Diese[rs]$", "Diese", None),
    ),
    # Personal pronouns
    (
        (r"^Ich$", "Wir", None),
        (r"^Du$", "Ihr", None),
        (r"^Er$", "Sie", None),
        (r"^Sie$", "Sie", None),
        (r"^Es$", "Sie", None),
        (r"^Mich$", "Uns", None),
        (r"^Dich$", "Euch", None),
        (r"^Ihn$", "Sie", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
        (r"^(Ge)", r"\1", None),
        (r"(gie)$", r"\1", None),
        (r"(au|ein|eit|er|[^i]en|[^i]el|chen|mus|tät|tik|tum|u)$", r"\1", None),
        (r"(mie|rie|sis|rin|ein|age|ern|ber|ion|inn|ben|äse|eis|hme|iss|hen|fer|gie|fen|her|ker|nie|mer|ler|men|ass"
         "|ner|per|rer|mus|abe|ter|ser|äle|hie|ger|tus|gen|ier|ver|zer)$", r"\1", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"(abe|ade|age|ale|ame|ane|are|ase|ate|che|cke|ede|ene|ere|ese|ffe|hie|hle|hme|hne|hre|hse|hte|ide|ife|ihe"
         "|ine|ise|ite|lge|lie|lle|mme|mpe|nde|nge|nie|nke|nne|nte|nze|ode|oge|one|ose|ote|pie|ppe|rbe|rde|rie|rke"
         "|rre|rte|sie|sse|ste|tie|tte|tze|ube|ude|ufe|uge|ule|ume|use|ute)$", r"\1n", None),
        (r"(ahr|akt|arn|bot|chs|ehl|eil|eim|eis|ekt|ell|erd|erk|ern|ert|ess|est|etz|eug"
         "|ekt|eur|ich|ick|ieb|eif|weg|ohr|ord|rot|tag|nkt|mpf|nat|nst|off|oot|lar|ruf"
         "|rzt|tiv|ieg|iel|iet|iff|ilm|ing|iss|itt|itz)$", r"\1e", None),
        (r"(aat|ahn|ant|aph|lei|ift|ist|enz|hrt|ion|orm|rei|tur|tor|uhr|ung|or|ei|schaft)$", r"\1en", None),
        (r"(rin|tin)$", r"\1nen", None),
        (r"(eld|ild|ind)$", r"\1er", None),
        (r"o(lz|rn)$", r"ö\1er", None),
        (r"a(ch|mt|nn|tt|us)$", r"ä\1er", None),
        (r"a(ng|nk|tz|um)$", r"ä\1e", None),
        (r"o(ck|hn|pf)$", r"ö\1e", None),
        (r"u(ch|ss)$", r"ü\1e", None),
        (r"a(ll|nd|ng|nk|tz|uf)$", r"ä\1e", None),
        (r"lan$", r"läne", None),
        (r"ag$", r"äge", None),
        (r"aal$", "äle", None),
        (r"(i)en$", r"\1um", None),
        (r"ika$", "ikum", None),
        (r"nis$", "nisse", None),
        (r"ra$", "raün", None),
        (r"bad$", "bäder", None),
        (r"hof$", "höfe", None),
        (r"zug$", "züge", None),
        (r"(ück)$", r"\1e", None),
        (r"(in)$", r"\1nen", None),
        (r"o$", r"os", None),
        (r"a$", r"en", None),
        (r"e$", r"en", None),
    ),
    # Assume that the plural takes -e
    (
        (r"$", "e", None),
    )
]

# For performance, compile the regular expressions once:
PLURAL_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in PLURAL_RULES]

# Suffix categories
PLURAL_CATEGORIES = {
    "uninflected": set(()),
    "uncountable": set(()),
    "nationalities": set(()),
}

SINGULAR_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^Diese$", "Dieses", None),
    ),
    # Personal pronouns
    (
        (r"^Wir$", "Ich", None),
        (r"^Ihr$", "Du", None),
        (r"^Sie$", "Er", None),
        (r"^Sie$", "Sie", None),
        (r"^Sie$", "Es", None),
        (r"^Uns$", "Mich", None),
        (r"^Euch$", "Dich", None),
        (r"^Sie$", "Ihn", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
        (r"^(Ge)", r"\1", None),
        (r"(gie)$", r"\1", None),
        (r"(au|ein|eit|er|[^i]en|[^i]el|chen|mus|tät|tik|tum|u)$", r"\1", None),
        (r"(mie|rie|sis|rin|ein|age|ern|ber|ion|inn|ben|äse|eis|hme|iss|hen|fer|gie|fen|her|ker"
         "|nie|mer|ler|men|ass|ner|per|rer|mus|abe|ter|ser|äle|hie|ger|tus|gen|ier|ver|zer)$", r"\1", None),
    ),
    # Irregular plural forms
    (
        (r"^Löwen$", "Löwe", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"innen$", r"in", None),
        (r"nisse$", "nis", None),
        (r"(ück|ühl)e$", r"\1", None),
        (r"(ühre|üte|üre|üse)n$", r"\1", None),
        (r"ü(ch|rm|hn)er$", r"u\1", None),
        (r"ü(st|ft|ch|rf|ng|nd|ss|rm)e$", r"u\1", None),
        (r"ä(nz|dt|rt|ck|hn|nk|ft|st|nd|ll|ht|ut|ss|tz|ng|mm|uf|um)e$", r"a\1", None),
        (r"(one|oge|ode|obe|ole|ose|ote)n$", r"\1", None),
        (r"(z|l)üge$", "\1ug", None),
        (r"ö(ck|pf|hn|ss)e$", r"o\1", None),
        (r"(h|t)ö(f|n)e$", "\1o\2", None),
        (r"(tte|mbe|lle|yse|rbe|hse|rve|rke|use|tie|ibe|ife|sse|gie|ete|rde|nce|ube|lbe|age|ane|ske|ede"
         "|gge|nte|mme|ige|nke|ine|see|ule|hre|abe|uge|lie|ase|ade|die|are|tze|hie|nde|hme|ffe|rme|ste"
         "|ame|hne|ume|nne|ale|mpe|mie|rte|rie|ude|lge|nge|ide|lke|ere|hle|ise|rne|pie|ihe|ese|äre|sie"
         "|ive|ppe|ene|lfe|nie|une|cke)n$", r"\1", None),
        (r"(tät|ahn|ent|hrt|ahl|uhr|sur|cht|kur|erz|sor|tat|ist|eit|rat|orm|ion|nis|ung|urt"
         "|enz|aat|aph|tür|son|tor|ant|tur)en$", r"\1", None),
        (r"ö(rn|lz|ch|rt)er$", r"o\1", None),
        (r"güter$", "gut", None),
        (r"bäder$", "bad", None),
        (r"räder$", "rad", None),
        (r"räser$", "ras", None),
        (r"läser$", "las", None),
        (r"läge$", "lag", None),
        (r"läne$", "lan", None),
        (r"(r|h)aün$", r"\1a", None),
        (r"räge$", "rag", None),
        (r"ä(nd|ch|ul|tt|nn|us|mt)er$", r"\1", None),
    ),
    # Assume that the plural takes
    (
        (r"(?!<(rr|rv|nz))(nen|en|n|e|er|s)$", "", None),
    )
]

# For performance, compile the regular expressions only once:
SINGULAR_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in SINGULAR_RULES]

# Suffix categories
SINGULAR_CATEGORIES = {
    "uninflected": PLURAL_CATEGORIES["uninflected"],
    "uncountable": PLURAL_CATEGORIES["uncountable"],
    "nationalities": PLURAL_CATEGORIES["nationalities"],
}
