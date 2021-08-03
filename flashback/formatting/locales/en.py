"""
Defines the English localization file for `flashback.formatting.singularize` and
`flashback.formatting.pluralize`.

Inspired by:

- https://github.com/clips/pattern/blob/master/pattern/text/en/inflect.py
"""

import regex


# Prepositions are used in compound words
PREPOSITIONS = set((
    "about", "before", "during", "of", "till",
    "above", "behind", "except", "off", "to",
    "across", "below", "for", "on", "under",
    "after", "beneath", "from", "onto", "until",
    "among", "beside", "in", "out", "unto",
    "around", "besides", "into", "over", "upon",
    "as", "at", "between", "near", "since", "with", "without",
    "athwart", "betwixt",
    "beyond",
    "but",
    "by",
))

PLURAL_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^a$|^an$", "some", None),
        (r"^this$", "these", None),
        (r"^that$", "those", None),
        (r"^any$", "all", None)
    ),
    # Possessive adjectives
    (
        (r"^my$", "our", None),
        (r"^your$", "your", None),
        (r"^thy$", "your", None),
        (r"^her$|^his$", "their", None),
        (r"^its$", "their", None),
        (r"^their$", "their", None)
    ),
    # Possessive pronouns
    (
        (r"^mine$", "ours", None),
        (r"^yours$", "yours", None),
        (r"^thine$", "yours", None),
        (r"^her$|^his$", "theirs", None),
        (r"^its$", "theirs", None),
        (r"^their$", "theirs", None)
    ),
    # Personal pronouns
    (
        (r"^i$", "we", None),
        (r"^me$", "us", None),
        (r"^myself$", "ourselves", None),
        (r"^you$", "you", None),
        (r"^thou$|^thee$", "ye", None),
        (r"^yourself$", "yourself", None),
        (r"^thyself$", "yourself", None),
        (r"^she$|^he$", "they", None),
        (r"^it$|^they$", "they", None),
        (r"^her$|^him$", "them", None),
        (r"^it$|^them$", "them", None),
        (r"^herself$", "themselves", None),
        (r"^himself$", "themselves", None),
        (r"^itself$", "themselves", None),
        (r"^themself$", "themselves", None),
        (r"^oneself$", "oneselves", None)
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"$", "", "nationalities"),
        (r"series$", "series", None),
        (r"fish$", "fish", None),
        (r"([- ])bass$", r"\1bass", None),
        (r"ois$", "ois", None),
        (r"sheep$", "sheep", None),
        (r"deer$", "deer", None),
        (r"pox$", "pox", None),
        (r"([a-z].*)ese$", r"\1ese", None),
        (r"itis$", "itis", None),
        (r"(fruct|gluc|galact|lact|ket|malt|rib|sacchar|cellul)ose$", r"\1ose", None)
    ),
    # Irregular plural forms
    (
        (r"atlas$", "atlases", None),
        (r"child$", "children", None),
        (r"corpus$", "corpora", None),
        (r"ephemeris$", "ephemerides", None),
        (r"genie$", "genii", None),
        (r"genus$", "genera", None),
        (r"graffito$", "graffiti", None),
        (r"loaf$", "loaves", None),
        (r"money$", "monies", None),
        (r"mongoose$", "mongooses", None),
        (r"mythos$", "mythoi", None),
        (r"octopus$", "octopuses", None),
        (r"opus$", "opuses", None),
        (r"^ox$", "oxen", None),
        (r"^penis$", "penises", None),
        (r"quiz$", "quizzes", None),
        (r"soliloquy$", "soliloquies", None),
        (r"testis$", "testes", None),
        (r"crisis$", "crises", None),
        (r"trilby$", "trilbys", None),
        (r"numen$", "numena", None),
        (r"occiput$", "occipita", None),
        (r"hoof$", "hooves", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"man$", "men", None),
        (r"person$", "people", None),
        (r"([lm])ouse$", r"\1ice", None),
        (r"tooth$", "teeth", None),
        (r"goose$", "geese", None),
        (r"foot$", "feet", None),
        (r"zoon$", "zoa", None),
        (r"([csx])is$", r"\1es", None),
    ),
    # Fully assimilated classical inflections
    (
        (r"ex$", "ices", "ex-ices"),
        (r"um$", "a", "um-a"),
        (r"on$", "a", "on-a"),
        (r"a$", "ae", "a-ae"),
    ),
    # Classical variants of modern inflections (e.g., stigmata, soprani).
    (
        (r"trix$", "trices", None),
        (r"eau$", "eaux", None),
        (r"ieu$", "ieu", None),
        (r"([iay])nx$", r"\1nges", None),
        (r"is$", "ises", "is-ises"),
        (r"us$", "i", "us-i"),
        (r"us$", "uses", "us-uses"),
        (r"o$", "i", "o-i"),
        (r"$", "im", "-im")
    ),
    # -ch, -sh and -ss and the s-singular group take -es in the plural
    (
        (r"([cs])h$", r"\1hes", None),
        (r"ss$", "sses", None),
        (r"x$", "xes", None),
        (r"s$", "ses", "s-singular")
    ),
    # -f or -fe sometimes take -ves in the plural
    (
        (r"([aeo]l)f$", r"\1ves", None),
        (r"([^d]ea)f$", r"\1ves", None),
        (r"arf$", "arves", None),
        (r"([nlw]i)fe$", r"\1ves", None),
        (r"(hoo|thie|shel)f$", r"\1ves", None)
    ),
    # -y takes -ys if preceded by a vowel, -ies otherwise
    (
        (r"([aeiou])y$", r"\1ys", None),
        (r"y$", "ies", None)
    ),
    # -o sometimes takes -os, -oes otherwise. -o preceded by a vowel takes -os
    (
        (r"o$", "os", "o-os"),
        (r"([aeiou])o$", r"\1os", None),
        (r"o$", "oes", None)
    ),
    # Assume that the plural takes -s
    (
        (r"(s)$", r"\1", None),
        (r"$", "s", None),
    )
]

# For performance, compile the regular expressions once:
PLURAL_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in PLURAL_RULES]

# Suffix categories
PLURAL_CATEGORIES = {
    "uninflected": set((
        "the", "yes", "no", "this", "next", "old",
        "beef", "bison", "debris", "headquarters", "news", "swine",
        "bream", "diabetes", "herpes", "pincers", "trout",
        "breeches", "djinn", "high-jinks", "pliers", "tuna",
        "britches", "eland", "homework", "proceedings", "whiting",
        "carp", "elk", "innings", "rabies", "wildebeest",
        "chassis", "flounder", "jackanapes", "salmon",
        "clippers", "gallows", "mackerel", "scissors",
        "cod", "graffiti", "measles",
        "contretemps", "mews", "shears", "wilderness",
        "corps", "mumps", "species", "christmas", "georgia",
        "north", "south", "east", "west", "jeans", "police",
    )),
    "uncountable": set((
        "stamina", "advice", "fruit", "ketchup", "meat", "sand",
        "bread", "furniture", "knowledge", "mustard", "software",
        "butter", "garbage", "love", "news", "understanding",
        "cannabis", "gravel", "luggage", "progress", "water",
        "cheese", "happiness", "mathematics", "research",
        "electricity", "information", "mayonnaise", "rice",
        "equipment", "blood",
    )),
    "nationalities": set((
        "german", "spanish", "british", "english", "scottish", "turkish", "dutch", "swiss",
    )),
    "s-singular": set((
        "acropolis", "caddis", "dais", "glottis", "pathos",
        "aegis", "canvas", "digitalis", "ibis", "pelvis",
        "alias", "chaos", "epidermis", "lens", "polis",
        "asbestos", "cosmos", "ethos", "mantis", "rhinoceros",
        "bathos", "gas", "marquis", "sassafras",
        "bias", "glottis", "metropolis", "trellis",
    )),
    "ex-ices": set((
        "codex", "murex", "silex", "apex", "index", "pontifex", "vertex",
        "cortex", "latex", "simplex", "vortex",
    )),
    "um-a": set((
        "agendum", "candelabrum", "desideratum", "extremum", "stratum",
        "bacterium", "datum", "erratum", "ovum", "aquarium", "emporium", "maximum", "optimum", "stadium",
        "compendium", "enconium", "medium", "phylum", "trapezium",
        "consortium", "gymnasium", "memorandum", "quantum", "ultimatum",
        "cranium", "honorarium", "millenium", "rostrum", "vacuum",
        "curriculum", "interregnum", "minimum", "spectrum", "velum",
        "dictum", "lustrum", "momentum", "speculum",
    )),
    "on-a": set((
        "aphelion", "hyperbaton", "perihelion",
        "asyndeton", "noumenon", "phenomenon",
        "criterion", "organon", "prolegomenon",
    )),
    "a-ae": set((
        "alga", "alumna", "vertebra", "abscissa", "aurora", "hyperbola", "nebula",
        "amoeba", "formula", "lacuna", "nova",
        "antenna", "hydra", "medusa", "parabola",
    )),
    "is-ises": set((
        "clitoris", "iris",
    )),
    "us-i": set((
        "focus", "nimbus", "succubus",
        "fungus", "nucleolus", "torus",
        "genius", "radius", "umbilicus",
        "incubus", "stylus", "uterus", "stimulus",
    )),
    "us-uses": set((
        "apparatus", "hiatus", "plexus", "status",
        "cantus", "impetus", "prospectus",
        "coitus", "nexus", "sinus", "bus", "virus",
    )),
    "o-i": set((
        "alto", "canto", "crescendo", "soprano",
        "basso", "contralto", "tempo",
    )),
    "-im": set((
        "cherub", "goy", "seraph",
    )),
    "o-os": set((
        "albino", "dynamo", "guano", "lumbago", "photo", "piano", "solo",
        "archipelago", "embryo", "inferno", "magneto", "pro",
        "armadillo", "fiasco", "jumbo", "manifesto", "quarto",
        "commando", "generalissimo", "medico", "rhino",
        "ditto", "ghetto", "lingo", "octavo", "stylo",
    )),
}

SINGULAR_RULES = [
    # Indefinite articles and demonstratives
    (
        (r"^some$", "a", None),
        (r"^these$", "this", None),
        (r"^those$", "that", None),
        (r"^all$", "any", None)
    ),
    # Possessive adjectives
    (
        (r"^our$", "my", None),
        (r"^your$", "your", None),
        (r"^their$", "its", None),
    ),
    # Possessive pronouns
    (
        (r"^ours$", "mine", None),
        (r"^yours$", "yours", None),
        (r"^theirs$", "its", None),
    ),
    # Personal pronouns
    (
        (r"^we$", "I", None),
        (r"^us$", "me", None),
        (r"^ourselves$", "myself", None),
        (r"^you$", "you", None),
        (r"^ye$", "thou", None),
        (r"^yourself$", "yourself", None),
        (r"^they$", "it", None),
        (r"^them$", "it", None),
        (r"^themselvesf$", "itself", None),
        (r"^oneselves$", "oneself", None)
    ),
    # Words that do not inflect
    (
        (r"$", "", "uninflected"),
        (r"$", "", "uncountable"),
        (r"^(\d{2}(?:\d{2})?s)$", r"\1", None),
        (r"series$", "series", None),
        (r"fish$", "fish", None),
        (r"([- ])bass$", r"\1bass", None),
        (r"ois$", "ois", None),
        (r"sheep$", "sheep", None),
        (r"deer$", "deer", None),
        (r"pox$", "pox", None),
        (r"([a-z].*)ese$", r"\1ese", None),
        (r"itis$", "itis", None),
        (r"(fruct|gluc|galact|lact|ket|malt|rib|sacchar|cellul)ose$", r"\1ose", None)
    ),
    # Irregular plural forms
    (
        (r"atla(ntes|ses)$", "atlas", None),
        (r"children$", "child", None),
        (r"corpora$", "corpus", None),
        (r"corpuses$", "corpus", None),
        (r"ephemerides$", "ephemeris", None),
        (r"genii$", "genie", None),
        (r"genera$", "genus", None),
        (r"graffiti$", "graffito", None),
        (r"loaves$", "loaf", None),
        (r"mon(ie|ey)s$", "money", None),
        (r"mongooses$", "mongoose", None),
        (r"mythoi$", "mythos", None),
        (r"octop(odes|uses|i)$", "octopus", None),
        (r"opuses$", "opus", None),
        (r"^oxen$", "ox", None),
        (r"^pen(ii|es|ises)?$", "penis", None),
        (r"quizzes$", "quiz", None),
        (r"soliloquies$", "soliloquy", None),
        (r"testes$", "testis", None),
        (r"crises$", "crisis", None),
        (r"trilbys$", "trilby", None),
        (r"numena$", "numen", None),
        (r"occipita$", "occiput", None),
        (r"shoes$", "shoe", None),
        (r"sexes$", "sex", None),
        (r"axes", "axe", None),
        (r"^helves$", "helve", None),
    ),
    # Irregular inflections for common suffixes
    (
        (r"men$", "man", None),
        (r"people$", "person", None),
        (r"([lm])ice$", r"\1ouse", None),
        (r"teeth$", "tooth", None),
        (r"geese$", "goose", None),
        (r"feet$", "foot", None),
        (r"zoa$", "zoon", None),
        (r"([csx])es$", r"\1is", "is-es")
    ),
    # Fully assimilated classical inflections
    (
        (r"ices$", "ex", "ex-ices"),
        (r"a$", "um", "um-a"),
        (r"a$", "on", "on-a"),
        (r"ae$", "a", "a-ae"),
    ),
    # Classical variants of modern inflections
    (
        (r"trices$", "trix", None),
        (r"eaux$", "eau", None),
        (r"ieu$", "ieu", None),
        (r"([iay])nges$", r"\1nx", None),  # FIXME: Does not handle "changes"/"exchanges"
        (r"ises$", "is", "is-ises"),
        (r"i$", "us", "us-i"),
        (r"uses$", "us", "us-uses"),
        (r"i$", "o", "o-i"),
        (r"im$", "", "-im"),
        (r"ies$", "ie", "ie-ies"),
    ),
    # -ch, -sh and -ss and the s-singular group take -es in the plural
    (
        (r"([cs])hes$", r"\1h", None),
        (r"sses$", "ss", None),
        (r"xes$", "x", None),
        (r"ses$", "s", "s-singular")
    ),
    # -f or -fe sometimes take -ves in the plural
    (
        (r"([aeo]l)ves$", r"\1f", None),
        (r"([^d]ea)ves$", r"\1f", None),
        (r"arves$", "arf", None),
        (r"([nlw]i)ves$", r"\1fe", None),
        (r"(hoo|thie|shel)ves$", r"\1f", None)
    ),
    # -y takes -ys if preceded by a vowel, -ies otherwise
    (
        (r"([aeiou])ys$", r"\1y", None),
        (r"ies$", "y", None)
    ),
    # -o sometimes takes -os, -oes otherwise. -o preceded by a vowel takes -os
    (
        (r"os$", "o", "o-os"),
        (r"([aeiou])os$", r"\1o", None),
        (r"oes$", "o", None)
    ),
    # Assume that the plural takes -s
    (
        (r"(?<!s)s$", "", None),
    )
]

# For performance, compile the regular expressions only once:
SINGULAR_RULES = [[(regex.compile(r[0]), r[1], r[2]) for r in grp] for grp in SINGULAR_RULES]

# Suffix categories
SINGULAR_CATEGORIES = {
    "uninflected": PLURAL_CATEGORIES["uninflected"],
    "uncountable": PLURAL_CATEGORIES["uncountable"],
    "nationalities": PLURAL_CATEGORIES["nationalities"],
    "s-singular": set((
        "acropolises", "caddises", "daises", "glottises", "pathoses",
        "aegises", "canvases", "digitalises", "ibises", "pelvises",
        "aliases", "chaoses", "epidermises", "lenses", "polises",
        "asbestoses", "cosmoses", "ethoses", "mantises", "rhinoceroses",
        "bathoses", "gases", "marquises", "sassafrases",
        "biases", "glottises", "metropolises", "trellises",
    )),
    "ie-ies": set((
        "alergies", "cuties", "hoagies", "newbies", "softies", "veggies",
        "aunties", "doggies", "hotties", "nighties", "sorties", "weenies",
        "beanies", "eyries", "indies", "oldies", "stoolies", "yuppies",
        "birdies", "freebies", "junkies", "pies", "sweeties", "zombies",
        "bogies", "goonies", "laddies", "pixies", "techies",
        "bombies", "groupies", "laramies", "quickies", "^ties",
        "collies", "hankies", "lingeries", "reveries", "toughies",
        "cookies", "hippies", "meanies", "rookies", "valkyries", "movies",
    )),
    "ex-ices": set((
        "codices", "murices", "silices", "apices", "indices", "pontifices", "vertices",
        "cortices", "latices", "simplices", "vortices",
    )),
    "um-a": set((
        "agenda", "candelabra", "desiderata", "extrema", "strata",
        "bacteria", "data", "errata", "ova", "aquaria", "emporia", "maxima", "optima", "stadia",
        "compendia", "enconia", "media", "phyla", "trapezia",
        "consortia", "gymnasia", "memoranda", "quanta", "ultimata",
        "crania", "honoraria", "millenia", "rostra", "vacua",
        "curricula", "interregna", "minima", "spectra", "vela",
        "dicta", "lustra", "momenta", "specula",
    )),
    "on-a": set((
        "aphelia", "hyperbata", "perihelia",
        "asyndeta", "noumena", "phenomena",
        "criteria", "organa", "prolegomena",
    )),
    "a-ae": set((
        "algae", "alumnae", "vertebrae", "abscissae", "aurorae", "hyperbolae", "nebulae",
        "amoebae", "formulae", "lacunae", "novae",
        "antennae", "hydrae", "medusae", "parabolae",
    )),
    "is-ises": set((
        "clitorises", "irises",
    )),
    "is-es": set((
        "analyses", "bases", "diagnoses", "parentheses", "prognoses", "synopses", "theses",
    )),
    "us-i": set((
        "foci", "nimbi", "succubi",
        "fungi", "nucleoli", "tori",
        "genii", "radii", "umbilici",
        "incubi", "styli", "uteri", "stimuli",
    )),
    "us-uses": set((
        "apparatuses", "hiatuses", "plexuses", "statuses",
        "cantuses", "impetuses", "prospectuses",
        "coituses", "nexuses", "sinuses", "buses", "viruses",
    )),
    "o-i": set((
        "alti", "canti", "crescendi", "soprani",
        "bassi", "contralti", "soli", "tempi",
    )),
    "-im": set((
        "cherubim", "goyim", "seraphim",
    )),
    "o-os": set((
        "albinos", "dynamos", "guanos", "lumbagos", "photos", "pianos", "solos",
        "archipelagos", "embryos", "infernos", "magnetos", "pros",
        "armadillos", "fiascos", "jumbos", "manifestos", "quartos",
        "commandos", "generalissimos", "medicos", "rhinos",
        "dittos", "ghettos", "lingos", "octavos", "stylos",
    )),
}
