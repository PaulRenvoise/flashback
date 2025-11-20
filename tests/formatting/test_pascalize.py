from flashback.formatting import camelize, kebabize, pascalize, snakeize


class TestPascalize:
    def test_lowercase(self) -> None:
        assert pascalize("stringio") == "Stringio"

    def test_snakecase(self) -> None:
        assert pascalize("var_name") == "VarName"

    def test_kebabcase(self) -> None:
        assert pascalize("long-url-path") == "LongUrlPath"

    def test_camelcase(self) -> None:
        assert pascalize("currentThread") == "CurrentThread"

    def test_pascalcase(self) -> None:
        assert pascalize("StringIO") == "StringIo"

    def test_protected_name(self) -> None:
        assert pascalize("_protected_name") == "_ProtectedName"

    def test_dunder_name(self) -> None:
        assert pascalize("__dunder_name__") == "__DunderName__"

    def test_lowercase_and_acronyms(self) -> None:
        assert pascalize("stringio", acronyms=["IO"]) == "StringIO"

    def test_snakecase_and_acronyms(self) -> None:
        assert pascalize("var_name", acronyms=["VA"]) == "VARName"

    def test_kebabcase_and_acronyms(self) -> None:
        assert pascalize("long-url-path", acronyms=["URL"]) == "LongURLPath"

    def test_camelcase_and_acronyms(self) -> None:
        assert pascalize("currentThread", acronyms=["THREAD"]) == "CurrentTHREAD"

    def test_pascalcase_and_acronyms(self) -> None:
        assert pascalize("StringIO", acronyms=["IO"]) == "StringIO"

    def test_camelize_revert(self) -> None:
        assert pascalize(camelize("CurrentThread")) == "CurrentThread"

    def test_kebabize_revert(self) -> None:
        assert pascalize(kebabize("LongUrlPath")) == "LongUrlPath"

    def test_snakeize_revert(self) -> None:
        assert pascalize(snakeize("VarName")) == "VarName"
