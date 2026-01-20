from flashback.formatting import camelize, kebabize, pascalize, snakeize


class TestCamelize:
    def test_lowercase(self) -> None:
        assert camelize("stringio") == "stringio"

    def test_snakecase(self) -> None:
        assert camelize("var_name") == "varName"

    def test_kebabcase(self) -> None:
        assert camelize("long-url-path") == "longUrlPath"

    def test_camelcase(self) -> None:
        assert camelize("currentThread") == "currentThread"

    def test_pascalcase(self) -> None:
        assert camelize("StringIO") == "stringIo"

    def test_protected_name(self) -> None:
        assert camelize("_protected_name") == "_protectedName"

    def test_dunder_name(self) -> None:
        assert camelize("__dunder_name__") == "__dunderName__"

    def test_lowercase_and_acronyms(self) -> None:
        assert camelize("stringio", acronyms=["IO"]) == "stringIO"

    def test_snakecase_and_acronyms(self) -> None:
        assert camelize("var_name", acronyms=["VA"]) == "VARName"

    def test_kebabcase_and_acronyms(self) -> None:
        assert camelize("long-url-path", acronyms=["URL"]) == "longURLPath"

    def test_camelcase_and_acronyms(self) -> None:
        assert camelize("currentThread", acronyms=["THREAD"]) == "currentTHREAD"

    def test_pascalcase_and_acronyms(self) -> None:
        assert camelize("StringIO", acronyms=["IO"]) == "stringIO"

    def test_snakeize_revert(self) -> None:
        assert camelize(snakeize("specialGuest")) == "specialGuest"

    def test_kebabize_revert(self) -> None:
        assert camelize(kebabize("varName")) == "varName"

    def test_pascalize_revert(self) -> None:
        assert camelize(pascalize("stringIo")) == "stringIo"
