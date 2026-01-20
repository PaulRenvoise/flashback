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


class TestSingularize:
    def test_languages(self) -> None:
        assert singularize("nights", language="en") == "night"
        assert singularize("nuits", language="fr") == "nuit"

    def test_invalid_language(self) -> None:
        with pytest.raises(NotImplementedError):
            singularize("", language="hu")

    def test_only_punctuation(self) -> None:
        assert singularize("??") == "??"

    def test_only_symbol(self) -> None:
        assert singularize("@#$%") == "@#$%"

    def test_only_numbers(self) -> None:
        assert singularize("123") == "123"

    def test_only_accents(self) -> None:
        assert singularize("é") == "é"

    def test_mixed_punctuation_symbol_number(self) -> None:
        assert singularize("!.:123$%") == "!.:123$%"

    class TestEnglish:
        def test_all_words(self, all_words) -> None:
            for singular, plural in all_words:
                assert singularize(plural, language="en") == singular

        def test_compound_words(self, compound_words) -> None:
            for singular, plural in compound_words:
                assert singularize(plural, language="en") == singular

        def test_exceptions(self, possessive_words) -> None:
            for singular, plural in possessive_words:
                assert singularize(plural, language="en") == singular
