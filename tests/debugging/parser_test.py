from unittest.mock import patch

import pytest

from flashback.debugging.parser import Parser

from .fixtures import mock_function


@pytest.fixture(scope="class")
def parser() -> Parser:
    return Parser(_offset=1)


class ParserTest:
    def parse_test(self, parser: Parser) -> None:
        filename, lineno, parsed_arguments, warning = parser.parse(None)

        assert filename == "tests/debugging/parser_test.py"
        assert lineno == 17
        assert parsed_arguments == [(None, None)]
        assert warning is None

    def parse_no_context_test(self, parser: Parser) -> None:  # noqa: ARG002
        filename, lineno, parsed_arguments, warning = eval("parser.parse(None)")

        assert filename == "<string>"
        assert lineno == 1
        assert parsed_arguments == [(None, None)]
        assert warning == "error parsing code, no code context found"

    @patch("flashback.debugging.parser.get_frameinfo")
    def parse_exception_test(self, mocked_get_frameinfo, parser: Parser) -> None:
        mocked_get_frameinfo.side_effect = ValueError("call stack is not deep enough")

        filename, lineno, parsed_arguments, warning = parser.parse(None)

        assert filename == "<unknown>"
        assert lineno == 0
        assert parsed_arguments == [(None, None)]
        assert warning == "error parsing code, call stack is not deep enough (ValueError)"

    def parse_simple_test(self, parser: Parser) -> None:
        a = 1

        _, _, parsed_arguments, _ = parser.parse(a)

        assert parsed_arguments == [("a", 1)]

    def parse_multiple_test(self, parser: Parser) -> None:
        a = 1
        b = [1, 2, 3]
        c = {"a": 1, "b": 2, "c": 3}
        d = "abc"

        _, _, parsed_arguments, _ = parser.parse(a, b, c, d, False)

        assert parsed_arguments == [
            ("a", 1),
            ("b", [1, 2, 3]),
            ("c", {"a": 1, "b": 2, "c": 3}),
            ("d", "abc"),
            (None, False),
        ]

    def parse_complex_test(self, parser: Parser) -> None:
        a = {"a": 1, "b": 2, "c": 3}
        b = [i + 1 for i in range(3)]

        _, _, parsed_arguments, _ = parser.parse(a["a"], b, mock_function(1, 2), "a" if a else "b", 1 != 0)  # noqa: PLR0133

        assert parsed_arguments == [
            ('a["a"]', 1),
            ("b", [1, 2, 3]),
            ("mock_function(1, 2)", 3),
            ('"a" if a else "b"', "a"),
            ("1 != 0", True),
        ]

    def parse_no_space_test(self, parser: Parser) -> None:
        a = 1
        b = [1, 2, 3]
        c = {"a": 1, "b": 2, "c": 3}

        _, _, parsed_arguments, _ = parser.parse(a, b, c)

        assert parsed_arguments == [("a", 1), ("b", [1, 2, 3]), ("c", {"a": 1, "b": 2, "c": 3})]

    def parse_newline_test(self, parser: Parser) -> None:
        _, _, parsed_arguments, _ = parser.parse(1)
        assert parsed_arguments == [(None, 1)]

    def parse_newlines_test(self, parser: Parser) -> None:
        _, _, parsed_arguments, warning = parser.parse(mock_function(1, 2))
        assert parsed_arguments == [("mock_function(1, 2)", 3)]
        assert warning is None

    def parse_nested_newlines_test(self, parser: Parser) -> None:
        _, _, parsed_arguments, warning = parser.parse(
            mock_function(mock_function(mock_function(mock_function(1, 2), 3), 4), 5),
        )
        assert parsed_arguments == [("mock_function(mock_function(mock_function(mock_function(1, 2), 3), 4), 5)", 15)]
        assert warning is None
