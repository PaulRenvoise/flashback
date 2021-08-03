"""
Defines the French localization file for `flashback.formatting.singularize` and
`flashback.formatting.pluralize`.

Inspired by:

- https://github.com/clips/pattern/blob/master/pattern/text/fr/inflect.py
"""

import regex


# Prepositions are used in compound words
PREPOSITIONS = set((
    "avant", "pendant", "durant", "dès", "de", "d'", "afin",
    "derrière", "devant", "travers", "sur", "sous",
    "après", "en-dedans", "dedans", "dehors", "en-dehors", "près", "auprès",
    "parmi", "outre", "sauf", "hors",
    "autour", "dans", "dessus", "dessous", "en-dessous",
    "chez", "entre", "envers", "vers", "depuis", "avec", "sans", "comme",
    "au-delà", "jusque", "voilà", "voici", "via",
    "en",
    "par"
))

PLURAL_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^une?$", "des", None),
        (r"^ce$", "ces", None),
        (r"^(le|la|l')$", "les", None),
    ),
    # Possessive adjectives
    (
        (r"^m(on|a)$", "mes", None),
        (r"^t(on|a)$", "tes", None),
        (r"^s(on|a)$", "ses", None),
    ),
    # Possessive pronouns
    (
        (r"^mien(ne)?$", r"mien\1s", None),
        (r"^tien(ne)?$", r"tien\1s", None),
        (r"^sien(ne)?$", r"sien\1s", None),
        (r"^notre$", "notres", None),
        (r"^votre$", "votres", None),
        (r"^leur$", "leurs", None),
    ),
    # Personal pronouns
    (
        (r"^(je|j')$", "nous", None),
        (r"^(tu|t')$", "vous", None),
        (r"^il$", "ils", None),
        (r"^elle$", "elles", None),
        (r"^moi$", "nous", None),
        (r"^toi$", "vous", None),
        (r"^lui$", "eux", None),
        (r"^moi-même$", "nous-même", None),
        (r"^toi-même$", "vous-même", None),
        (r"^lui-même$", "eux-même", None),
        (r"^elle-même$", "elles-même", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
    ),
    # Irregular plural forms
    (
        (r"^aïeul$", "aïeux", None),
        (r"^ail$", "aulx", None),
        (r"ciel$", "cieux", None),
        (r"oeil$", "yeux", None),
        (r"vieil$", "vieux", None),
        (r"^laquelle$", "lesquelles", None),
        (r"^lequel$", "lesquels", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"eu$", "eus", "eu-eus"),
        (r"ou$", "oux", "ou-oux"),
        (r"al$", "als", "al-als"),
        (r"au$", "aus", "au-aus"),
        (r"ail$", "aux", "ail-aux"),
        (r"(au|eu)$", r"\1x", None),
        (r"al$", "aux", None),
    ),
    # Assume that the plural takes -s
    (
        (r"(s|x|z)$", r"\1", None),
        (r"$", "s", None),
    )
]

# For performance, compile the regular expressions once:
PLURAL_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in PLURAL_RULES]

# Suffix categories
PLURAL_CATEGORIES = {
    "uninflected": set((
        "oui", "non",
        "cette", "cet",
        "débris", "news", "hèrpes", "chassis", "ciseaux",
        "graffiti", "contretemps", "corps", "mois", "os",
        "ananas", "nord", "sud", "est", "ouest",
        "y", "droite", "gauche",
        "brebis", "bus", "cas",
        "fils", "gaz", "héros",
        "houx", "index", "lynx",
        "matelas", "nez", "puits",
        "prix", "quartz", "quiz",
        "rhinocéros", "sas",
        "souris", "taux", "malappris",
        "bas", "las", "hélas", "m'",
        "qui", "que", "quoi", "quand", "où",
        "fois", "radis", "codex",
    )),
    "uncountable": set((
        "ketchup", "riz", "temps", "poésie", "sang",
    )),
    "nationalities": set((
        "français", "anglais", "japonais", "hollandais", "portugais",
        "écossais", "irlandais", "polonais", "pakistanais", "albanais",
        "taïwanais", "maltais", "congolais", "néerlandais", "néo-zélandais",
        "thaïlandais", "soudanais", "sénégalais", "libanais",
    )),
    "eu-eus": set((
        "beu", "bisteu", "bleu",
        "émeu", "enfeu", "eu",
        "neuneu", "pneu", "rebeu"
    )),
    "ou-oux": set((
        "bijou", "caillou", "chou",
        "genou", "hibou", "joujou",
        "pou", "ripou",
    )),
    "al-als": set((
        "banal", "bancal", "fatal", "fractal", "morfal",
        "naval", "aéronaval", "natal", "anténatal", "néonatal",
        "périnatal", "postnatal", "prénatal", "tonal", "atonal",
        "bitonal", "polytonal", "acétal", "ammonal", "aval",
        "bal", "barbital", "cal", "captal", "carnaval",
        "cérémonial", "chacal", "chloral", "chrysocal", "copal",
        "dial", "dispersal", "éthanal", "festival", "foiral",
        "furfural", "futal", "gal", "galgal", "gardénal",
        "graal", "joual", "kraal", "kursaal", "matorral",
        "mescal", "mezcal", "méthanal", "minerval", "mistral",
        "nopal", "pal", "pascal", "penthotal", "phénobarbital",
        "pipéronal", "raval", "récital", "régal", "rétinal",
        "rital", "roberval", "roseval", "salicional", "sal",
        "sandal", "santal", "saroual", "sial", "sisal",
        "sonal", "tagal", "tefal", "tergal", "thiopental",
        "tical", "tincal", "véronal", "zicral", "caracal",
        "chacal", "gavial", "gayal", "narval", "quetzal",
        "rorqual", "serval", "metical", "rial", "riyal",
        "ryal", "corral", "deal", "goal", "revival",
        "serial", "spiritual", "trial", "cantal", "emmental",
        "emmenthal",
    )),
    "au-aus": set((
        "antitau", "berimbau", "burgau",
        "crau", "donau", "grau",
        "hessiau", "jautereau", "jotterau",
        "karbau", "kérabau", "landau",
        "restau", "sarrau", "saun gau",
        "senau", "tamarau", "tau",
        "uchau", "unau", "wau"
    )),
    "au-aux": set((
        "bitoniau", "biomatériau", "bau", "atriau", "aloyau",
        "affutiau", "au", "bestiau", "boucau", "boyau",
        "cabillau", "tussau", "tuyau", "vau", "viperiau",
        "fabliau", "esquimau", "coyau", "carnau", "etau",
        "flutiau", "hoyau", "huhau", "gruau", "gluau",
        "ibijau", "joyau", "matériau", "merbau", "micronoyau",
        "morvandiau", "nanomatériau", "nilgau", "nobliau", "noyau",
        "touchau", "surbau", "salopiau", "rafiau", "pilau",
        "sauteriau",
    )),
    "ail-aux": set((
        "aspirail", "corail", "bail",
        "émail", "fermail", "gemmail",
        "soupirail", "travail", "vantail", "vitrail",
    )),
}


SINGULAR_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^des$", "un", None),
        (r"^ces$", "ce", None),
        (r"^les$", "le", None),
    ),
    # Possessive adjectives
    (
        (r"^mes$", "mon", None),
        (r"^tes$", "ton", None),
        (r"^ses$", "son", None),
    ),
    # Possessive pronouns
    (
        (r"^mien(ne)s?$", r"mien\1", None),
        (r"^tien(ne)s?$", r"tien\1", None),
        (r"^sien(ne)s?$", r"sien\1", None),
        (r"^notres$", "notre", None),
        (r"^votres$", "votre", None),
        (r"^nos$", "notre", None),
        (r"^vos$", "votre", None),
        (r"^leurs$", "leur", None),
    ),
    # Personal pronouns
    (
        (r"^nous$", "je", None),
        (r"^vous$", "tu", None),
        (r"^elles$", "elle", None),
        (r"^ils$", "il", None),
        (r"^eux$", "lui", None),
        (r"^nous$", "moi", None),
        (r"^vous$", "toi", None),
        (r"^nous-même$", "moi-même", None),
        (r"^vous-même$", "toi-même", None),
        (r"^eux-même$", "lui-même", None),
        (r"^elles-même$", "elle-même", None),
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
    ),
    # Irregular plural forms
    (
        (r"('|’)$", "e", None),
        (r"^aïeux$", "aïeul", None),
        (r"^aulx$", "ail", None),
        (r"cieux$", "ciel", None),
        (r"yeux$", "oeil", None),
        (r"vieux$", "vieil", None),
        (r"^lesquelles$", "laquelle", None),
        (r"^lesquels$", "lequel", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"eus$", "eu", "eu-eus"),
        (r"oux$", "ou", "ou-oux"),
        (r"als$", "al", "al-als"),
        (r"aus$", "au", "au-aus"),
        (r"aux$", "au", "au-aux"),
        (r"aux$", "ail", "ail-aux"),
        (r"(eau|eu)x$", r"\1", None),
        (r"aux$", "al", None),
    ),
    # Assume that the plural takes -s
    (
        (r"(?<!ai)s$", "", None),
    )
]

# For performance, compile the regular expressions once:
SINGULAR_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in SINGULAR_RULES]

# Suffix categories
SINGULAR_CATEGORIES = {
    "uninflected": PLURAL_CATEGORIES["uninflected"],
    "uncountable": PLURAL_CATEGORIES["uncountable"],
    "nationalities": PLURAL_CATEGORIES["nationalities"],
    "eu-eus": set((
        "beus", "bisteus", "bleus",
        "émeus", "enfeus", "eus",
        "neuneus", "pneus", "rebeus"
    )),
    "ou-oux": set((
        "bijoux", "cailloux", "choux",
        "genoux", "hiboux", "jouxjoux",
        "poux", "ripoux",
    )),
    "al-als": set((
        "banals", "bancals", "fatals", "fractals", "morfals",
        "navals", "aéronavals", "natals", "anténatals", "néonatals",
        "périnatals", "postnatals", "prénatals", "tonals", "atonals",
        "bitonals", "polytonals", "acétals", "ammonals", "avals",
        "bals", "barbitals", "cals", "captals", "carnavals",
        "cérémonials", "chacals", "chlorals", "chrysocals", "copals",
        "dials", "dispersals", "éthanals", "festivals", "foirals",
        "furfurals", "futals", "gals", "galsgals", "gardénals",
        "graals", "jouals", "kraals", "kursaals", "matorrals",
        "mescals", "mezcals", "méthanals", "minervals", "mistrals",
        "nopals", "pals", "pascals", "penthotals", "phénobarbitals",
        "pipéronals", "ravals", "récitals", "régals", "rétinals",
        "ritals", "robervals", "rosevals", "salsicionals", "sals",
        "sandals", "santals", "sarouals", "sials", "sisals",
        "sonals", "tagals", "tefals", "tergals", "thiopentals",
        "ticals", "tincals", "véronals", "zicrals", "caracals",
        "chacals", "gavials", "gayals", "narvals", "quetzals",
        "rorquals", "servals", "meticals", "rials", "riyals",
        "ryals", "corrals", "deals", "goals", "revivals",
        "serials", "spirituals", "trials", "cantals", "emmentals",
        "emmenthals",
    )),
    "au-aus": set((
        "antitaus", "berimbaus", "burgaus",
        "craus", "donaus", "graus",
        "hessiaus", "jaustereaus", "jotteraus",
        "karbaus", "kérabaus", "landaus",
        "restaus", "sarraus", "sausn gaus",
        "senaus", "tamaraus", "taus",
        "uchaus", "unaus", "waus"
    )),
    "au-aux": set((
        "bitoniaux", "biomateriaux", "baux", "atriaux", "aloyaux",
        "affutiaux", "aux", "bestiaux", "boucaux", "boyaux",
        "cabillaux", "tussaux", "tuyaux", "vaux", "viperiaux",
        "fabliaux", "esquimaux", "coyaux", "carnaux", "etaux",
        "flutiaux", "hoyaux", "huhaux", "gruaux", "gluaux",
        "ibijaux", "joyaux", "materiaux", "merbaux", "micronoyaux",
        "morvandiaux", "nanomateriaux", "nilgaux", "nobliaux", "noyaux",
        "touchaux", "surbaux", "salopiaux", "rafiaux", "pilaux",
        "sauxteriaux",
    )),
    "ail-aux": set((
        "aspiraux", "coraux", "baux",
        "émaux", "fermaux", "gemmaux",
        "soupiraux", "travaux", "vantaux", "vitraux",
    )),
}
