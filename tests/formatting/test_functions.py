# pylint: disable=no-self-use,redefined-outer-name

import pytest

from copernicus.formatting import *


class TestOxfordJoin():
    def test_zero_items(self):
        assert oxford_join([]) == ''

    def test_one_item(self):
        assert oxford_join(['one']) == 'one'

    def test_two_items(self):
        assert oxford_join(['one', 'two']) == 'one and two'

    def test_three_items(self):
        assert oxford_join(['one', 'two', 'three']) == 'one, two, and three'

    def test_two_items_and_sep_and_couple_sep(self):
        assert oxford_join(['one', 'two'], sep='; ', couple_sep=' or ') == 'one or two'

    def test_three_items_and_sep_and_last_sep(self):
        assert oxford_join(['one', 'two', 'three'], sep='; ', last_sep='; plus ') == 'one; two; plus three'

    def test_two_items_and_quotes(self):
        assert oxford_join(['one', 'two'], quotes=True) == "'one' and 'two'"


class TestTransliterate():
    def test_unicode_only_chars(self):
        origin = '\u2124\U0001d552\U0001d55c\U0001d552\U0001d55b \U0001d526\U0001d52a\U0001d51e \U0001d4e4\U0001d4f7\U0001d4f2\U0001d4ec\U0001d4f8\U0001d4ed\U0001d4ee \U0001d4c8\U0001d4c5\u212f\U0001d4b8\U0001d4be\U0001d4bb\U0001d4be\U0001d4c0\U0001d4b6\U0001d4b8\U0001d4be\U0001d4bf\u212f \U0001d59f\U0001d586 \U0001d631\U0001d62a\U0001d634\U0001d622\U0001d637\U0001d626?!'    # pylint: disable=line-too-long
        target = 'Zakaj ima Unicode specifikacije za pisave?!'

        assert transliterate(origin) == target

    def test_ascii_only_chars(self):
        origin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        target = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

        assert transliterate(origin) == target

    def test_mixed_chars(self):
        origin = 'PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ PĚL ĎÁBELSKÉ ÓDY'
        target = 'PRILIS ZLUTOUCKY KUN PEL DABELSKE ODY'

        assert transliterate(origin) == target

    def test_mixed_chars_and_keep_case(self):
        origin = 'Je vais au ch\u00e2teau de Joséphine'
        target = 'je vais au chateau de josephine'

        assert transliterate(origin, keep_case=False) == target


class TestCamelize():
    def test_lowercase(self):
        assert camelize('party') == 'Party'

    def test_snakecase(self):
        assert camelize('special_guest') == 'SpecialGuest'

    def test_camelcase(self):
        assert camelize('NotFunException') == 'NotFunException'

    def test_lowercase_and_acronyms(self):
        assert camelize('svcclassifier', acronyms=['SVC']) == 'SVCClassifier'

    def test_lowercase_and_weird_acronyms(self):
        assert camelize('https', acronyms=['HTTP']) == 'HTTPS'

    def test_lowercase_and_single_acronyms(self):
        assert camelize('http', acronyms=['HTTP']) == 'HTTP'

    def test_snakecase_and_acronyms(self):
        assert camelize('deep_custom_svc_classifier', acronyms=['DEep', 'SVC']) == 'DEepCustomSVCClassifier'

    def test_snakecase_and_weird_acronyms(self):
        assert camelize('application_controller', acronyms=['APP']) == 'APPLicationController'

    def test_lowercase_and_missing_acronyms(self):
        assert camelize('application', acronyms=['BSD']) == 'Application'

    def test_snakeize_revert(self):
        assert camelize(snakeize('SpecialGuest')) == 'SpecialGuest'

    def test_snakeize_revert_and_acronyms(self):
        acronyms = ['HTML']

        assert camelize(snakeize('HTMLTidyGenerator', acronyms=acronyms), acronyms=acronyms) == 'HTMLTidyGenerator'


class TestSnakeize():
    def test_lowercase(self):
        assert snakeize('party') == 'party'

    def test_snakecase(self):
        assert snakeize('special_guest') == 'special_guest'

    def test_camelcase(self):
        assert snakeize('NotFunException') == 'not_fun_exception'

    def test_lowercase_and_acronyms(self):
        assert snakeize('svcclassifier', acronyms=['SVC']) == 'svc_classifier'

    def test_snakecase_and_acronyms(self):
        assert snakeize('svc_classifier', acronyms=['SVC']) == 'svc_classifier'

    def test_snakecase_and_weird_acronyms(self):
        assert snakeize('application_controller', acronyms=['APP']) == 'app_lication_controller'

    def test_camelcase_and_acronyms(self):
        assert snakeize('SVCClassifier', acronyms=['SVC']) == 'svc_classifier'

    def test_camelcase_and_weird_acronyms(self):
        assert snakeize('HTTPS', acronyms=['HTTP']) == 'http_s'

    def test_lowercase_and_missing_acronyms(self):
        assert snakeize('https', acronyms=['BDS']) == 'https'

    def test_camelize_revert(self):
        assert snakeize(camelize('special_guest')) == 'special_guest'

    def test_camelize_revert_and_acronyms(self):
        acronyms = ['HTML']

        assert snakeize(camelize('html_tidy_generator', acronyms=acronyms), acronyms=acronyms) == 'html_tidy_generator'


class TestParameterize():
    def test_one_word(self):
        assert parameterize('Guy') == 'guy'

    def test_multiple_words(self):
        assert parameterize('Donald E. Knuth') == 'donald-e-knuth'

    def test_bad_characters(self):
        assert parameterize('*(o.o)*') == 'o-o'

    def test_underscores(self):
        assert parameterize('int object_index = 0') == 'int-object_index-0'

    def test_multiple_separators(self):
        assert parameterize('squeeze     all!') == 'squeeze-all'

    def test_unicode(self):
        assert parameterize('PŘÍLIŠ ŽLUŤOUČKÝ') == 'prilis-zlutoucky'

    def test_multiple_words_and_keep_case(self):
        assert parameterize('Donald E. Knuth', keep_case=True) == 'Donald-E-Knuth'

    def test_multiple_words_and_sep(self):
        assert parameterize('Donald E. Knuth', sep='//') == 'donald//e//knuth'

    def test_multiple_words_and_sep2(self):
        assert parameterize('Donald E. Knuth', sep='') == 'donaldeknuth'


class TestOrdinalize():
    def test_st(self):
        assert ordinalize(1) == '1st'

    def test_nd(self):
        assert ordinalize(2) == '2nd'

    def test_rd(self):
        assert ordinalize(3) == '3rd'

    def test_th(self):
        assert ordinalize(8) == '8th'

    def test_tens(self):
        assert ordinalize(25) == '25th'

    def test_hundreds(self):
        assert ordinalize(103) == '103rd'

    def test_thousands(self):
        assert ordinalize(1241) == '1241st'

    def test_ten_thousands(self):
        assert ordinalize(20602) == '20602nd'

    def test_negative(self):
        assert ordinalize(-1) == '-1st'


class TestAdverbize():
    def test_once(self):
        assert adverbize(1) == 'once'

    def test_twice(self):
        assert adverbize(2) == 'twice'

    def test_thrice(self):
        assert adverbize(3) == 'thrice'

    def test_times(self):
        assert adverbize(8) == '8 times'

    def test_tens(self):
        assert adverbize(25) == '25 times'

    def test_hundreds(self):
        assert adverbize(103) == '103 times'

    def test_thousands(self):
        assert adverbize(1241) == '1241 times'

    def test_ten_thousands(self):
        assert adverbize(20602) == '20602 times'

    def test_negative(self):
        assert adverbize(-1) == '-1 times'


@pytest.fixture
def all_words():
    items = (
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
        ("taxi", "taxis"), # prevents regression
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

    return items


@pytest.fixture
def compound_words():
    items = (
        ("asian-american", "asian-americans"),
        ("vice-president", "vice-presidents"),
        ("dry-cleaning", "dry-cleanings"),
        ("runner-up", "runner-ups"),
        ("has-been", "has-beens"),
        ("mother-in-law", "mothers-in-law"),
    )

    return items


@pytest.fixture
def possessive_words():
    items = (
        ("dog's", "dogs'"),
        ("sheep's", "sheep's"),
        ("class'", "classes'"),
    )

    return items

class TestSingularize():
    def test_languages(self):
        assert singularize('nights', language='en') == 'night'
        assert singularize('nuits', language='fr') == 'nuit'

    def test_invalid_language(self):
        with pytest.raises(NotImplementedError):
            singularize('', language='hu')

    def test_only_punctuation(self):
        assert singularize('??') == '??'

    def test_only_symbol(self):
        assert singularize('@#$%') == '@#$%'

    def test_only_numbers(self):
        assert singularize('123') == '123'

    def test_only_accents(self):
        assert singularize('é') == 'é'

    def test_mixed_punctuation_symbol_number(self):
        assert singularize('!.:123$%') == '!.:123$%'

    class TestEnglish():
        def test_all_words(self, all_words):
            for singular, plural in all_words:
                assert singularize(plural, language='en') == singular

        def test_compound_words(self, compound_words):
            for singular, plural in compound_words:
                assert singularize(plural, language='en') == singular

        def test_exceptions(self, possessive_words):
            for singular, plural in possessive_words:
                assert singularize(plural, language='en') == singular


class TestPluralize():
    def test_languages(self):
        assert pluralize('night', language='en') == 'nights'
        assert pluralize('nuit', language='fr') == 'nuits'

    def test_invalid_language(self):
        with pytest.raises(NotImplementedError):
            pluralize('', language='hu')

    def test_only_punctuation(self):
        assert pluralize('??') == '??'

    def test_only_symbol(self):
        assert pluralize('@#$%') == '@#$%'

    def test_only_numbers(self):
        assert pluralize('123') == '123'

    def test_mixed_punctuation_symbol_number(self):
        assert pluralize('!.:123$%') == '!.:123$%'

    class TestEnglish():
        def test_all_words(self, all_words):
            for singular, plural in all_words:
                assert pluralize(singular, language='en') == plural

        def test_compound_words(self, compound_words):
            for singular, plural in compound_words:
                assert pluralize(singular, language='en') == plural

        def test_possessive_words(self, possessive_words):
            for singular, plural in possessive_words:
                assert pluralize(singular, language='en') == plural
