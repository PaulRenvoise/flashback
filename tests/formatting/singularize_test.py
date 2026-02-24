import pytest

from flashback.formatting import singularize


@pytest.fixture
def all_words() -> tuple[tuple[str, str], ...]:
    return (
        ("search", "searches"),
        ("switch", "switches"),
        ("fix", "fixes"),
        ("box", "boxes"),
        ("process", "processes"),
        ("address", "addresses"),
        ("case", "cases"),
        ("stack", "stacks"),
        ("wish", "wishes"),
        ("fish", "fish"),
        ("jeans", "jeans"),
        ("money", "monies"),
        ("category", "categories"),
        ("query", "queries"),
        ("ability", "abilities"),
        ("agency", "agencies"),
        ("movie", "movies"),
        ("archive", "archives"),
        ("index", "indices"),
        ("wife", "wives"),
        ("safe", "safes"),
        ("half", "halves"),
        ("move", "moves"),
        ("salesperson", "salespeople"),
        ("person", "people"),
        ("spokesman", "spokesmen"),
        ("man", "men"),
        ("woman", "women"),
        ("basis", "bases"),
        ("diagnosis", "diagnoses"),
        ("datum", "data"),
        ("medium", "media"),
        ("stadium", "stadia"),
        ("analysis", "analyses"),
        ("child", "children"),
        ("experience", "experiences"),
        ("day", "days"),
        ("comment", "comments"),
        ("foobar", "foobars"),
        ("newsletter", "newsletters"),
        ("news", "news"),
        ("series", "series"),
        ("miniseries", "miniseries"),
        ("species", "species"),
        ("quiz", "quizzes"),
        ("perspective", "perspectives"),
        ("ox", "oxen"),
        ("photo", "photos"),
        ("buffalo", "buffaloes"),
        ("tomato", "tomatoes"),
        ("dwarf", "dwarves"),
        ("elf", "elves"),
        ("information", "information"),
        ("equipment", "equipment"),
        ("bus", "buses"),
        ("status", "statuses"),
        ("mouse", "mice"),
        ("louse", "lice"),
        ("house", "houses"),
        ("octopus", "octopuses"),
        ("virus", "viruses"),
        ("alias", "aliases"),
        ("portfolio", "portfolios"),
        ("vertex", "vertices"),
        ("matrix", "matrices"),
        ("axe", "axes"),
        ("taxi", "taxis"),  # prevents regression
        ("testis", "testes"),
        ("crisis", "crises"),
        ("rice", "rice"),
        ("shoe", "shoes"),
        ("horse", "horses"),
        ("prize", "prizes"),
        ("edge", "edges"),
        ("database", "databases"),
        ("slice", "slices"),
        ("police", "police"),
    )


@pytest.fixture
def compound_words() -> tuple[tuple[str, str], ...]:
    return (
        ("asian-american", "asian-americans"),
        ("vice-president", "vice-presidents"),
        ("dry-cleaning", "dry-cleanings"),
        ("runner-up", "runner-ups"),
        ("has-been", "has-beens"),
        ("mother-in-law", "mothers-in-law"),
    )


@pytest.fixture
def possessive_words() -> tuple[tuple[str, str], ...]:
    return (
        ("dog's", "dogs'"),
        ("sheep's", "sheep's"),
        ("class'", "classes'"),
    )


class SingularizeTest:
    def languages_test(self) -> None:
        assert singularize("nights", language="en") == "night"
        assert singularize("nuits", language="fr") == "nuit"

    def invalid_language_test(self) -> None:
        with pytest.raises(NotImplementedError):
            singularize("", language="hu")

    def only_punctuation_test(self) -> None:
        assert singularize("??") == "??"

    def only_symbol_test(self) -> None:
        assert singularize("@#$%") == "@#$%"

    def only_numbers_test(self) -> None:
        assert singularize("123") == "123"

    def only_accents_test(self) -> None:
        assert singularize("é") == "é"

    def mixed_punctuation_symbol_number_test(self) -> None:
        assert singularize("!.:123$%") == "!.:123$%"

    class EnglishTest:
        def all_words_test(self, all_words) -> None:
            for singular, plural in all_words:
                assert singularize(plural, language="en") == singular

        def compound_words_test(self, compound_words) -> None:
            for singular, plural in compound_words:
                assert singularize(plural, language="en") == singular

        def possessive_words_test(self, possessive_words) -> None:
            for singular, plural in possessive_words:
                assert singularize(plural, language="en") == singular
