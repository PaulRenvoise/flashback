from flashback.formatting import camelize, kebabize, pascalize, snakeize


class PascalizeTest:
    def lowercase_test(self) -> None:
        assert pascalize("stringio") == "Stringio"

    def snakecase_test(self) -> None:
        assert pascalize("var_name") == "VarName"

    def kebabcase_test(self) -> None:
        assert pascalize("long-url-path") == "LongUrlPath"

    def camelcase_test(self) -> None:
        assert pascalize("currentThread") == "CurrentThread"

    def pascalcase_test(self) -> None:
        assert pascalize("StringIO") == "StringIo"

    def protected_name_test(self) -> None:
        assert pascalize("_protected_name") == "_ProtectedName"

    def dunder_name_test(self) -> None:
        assert pascalize("__dunder_name__") == "__DunderName__"

    def empty_acronyms_test(self) -> None:
        assert pascalize("stringio", acronyms=[]) == "Stringio"

    def lowercase_and_acronyms_test(self) -> None:
        assert pascalize("stringio", acronyms=["IO"]) == "StringIO"

    def snakecase_and_acronyms_test(self) -> None:
        assert pascalize("var_name", acronyms=["VA"]) == "VARName"

    def kebabcase_and_acronyms_test(self) -> None:
        assert pascalize("long-url-path", acronyms=["URL"]) == "LongURLPath"

    def camelcase_and_acronyms_test(self) -> None:
        assert pascalize("currentThread", acronyms=["THREAD"]) == "CurrentTHREAD"

    def pascalcase_and_acronyms_test(self) -> None:
        assert pascalize("StringIO", acronyms=["IO"]) == "StringIO"

    def camelize_revert_test(self) -> None:
        assert pascalize(camelize("CurrentThread")) == "CurrentThread"

    def kebabize_revert_test(self) -> None:
        assert pascalize(kebabize("LongUrlPath")) == "LongUrlPath"

    def snakeize_revert_test(self) -> None:
        assert pascalize(snakeize("VarName")) == "VarName"
