# pylint: disable=no-self-use

from flashback.formatting import camelize, kebabize, pascalize, snakeize


class TestPascalize:
    def test_lowercase(self):
        assert pascalize("stringio") == "Stringio"

    def test_snakecase(self):
        assert pascalize("var_name") == "VarName"

    def test_kebabcase(self):
        assert pascalize("long-url-path") == "LongUrlPath"

    def test_camelcase(self):
        assert pascalize("currentThread") == "CurrentThread"

    def test_pascalcase(self):
        assert pascalize("StringIO") == "StringIo"

    def test_protected_name(self):
        assert pascalize("_protected_name") == "_ProtectedName"

    def test_dunder_name(self):
        assert pascalize("__dunder_name__") == "__DunderName__"

    def test_lowercase_and_acronyms(self):
        assert pascalize("stringio", acronyms=["IO"]) == "StringIO"

    def test_snakecase_and_acronyms(self):
        assert pascalize("var_name", acronyms=["VA"]) == "VARName"

    def test_kebabcase_and_acronyms(self):
        assert pascalize("long-url-path", acronyms=["URL"]) == "LongURLPath"

    def test_camelcase_and_acronyms(self):
        assert pascalize("currentThread", acronyms=["THREAD"]) == "CurrentTHREAD"

    def test_pascalcase_and_acronyms(self):
        assert pascalize("StringIO", acronyms=["IO"]) == "StringIO"

    def test_camelize_revert(self):
        assert pascalize(camelize("CurrentThread")) == "CurrentThread"

    def test_kebabize_revert(self):
        assert pascalize(kebabize("LongUrlPath")) == "LongUrlPath"

    def test_snakeize_revert(self):
        assert pascalize(snakeize("VarName")) == "VarName"
