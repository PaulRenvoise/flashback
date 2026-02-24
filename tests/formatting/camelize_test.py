from flashback.formatting import camelize, kebabize, pascalize, snakeize


class CamelizeTest:
    def lowercase_test(self) -> None:
        assert camelize("stringio") == "stringio"

    def snakecase_test(self) -> None:
        assert camelize("var_name") == "varName"

    def kebabcase_test(self) -> None:
        assert camelize("long-url-path") == "longUrlPath"

    def camelcase_test(self) -> None:
        assert camelize("currentThread") == "currentThread"

    def pascalcase_test(self) -> None:
        assert camelize("StringIO") == "stringIo"

    def protected_name_test(self) -> None:
        assert camelize("_protected_name") == "_protectedName"

    def dunder_name_test(self) -> None:
        assert camelize("__dunder_name__") == "__dunderName__"

    def empty_acronyms_test(self) -> None:
        assert camelize("stringio", acronyms=[]) == "stringio"

    def lowercase_and_acronyms_test(self) -> None:
        assert camelize("stringio", acronyms=["IO"]) == "stringIO"

    def snakecase_and_acronyms_test(self) -> None:
        assert camelize("var_name", acronyms=["VA"]) == "VARName"

    def kebabcase_and_acronyms_test(self) -> None:
        assert camelize("long-url-path", acronyms=["URL"]) == "longURLPath"

    def camelcase_and_acronyms_test(self) -> None:
        assert camelize("currentThread", acronyms=["THREAD"]) == "currentTHREAD"

    def pascalcase_and_acronyms_test(self) -> None:
        assert camelize("StringIO", acronyms=["IO"]) == "stringIO"

    def snakeize_revert_test(self) -> None:
        assert camelize(snakeize("specialGuest")) == "specialGuest"

    def kebabize_revert_test(self) -> None:
        assert camelize(kebabize("varName")) == "varName"

    def pascalize_revert_test(self) -> None:
        assert camelize(pascalize("stringIo")) == "stringIo"
