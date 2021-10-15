# pylint: disable=no-self-use,redefined-outer-name,invalid-name

import sys

import pytest
from mock import patch

from flashback.debugging.parser import Parser

from .fixtures import mock_function


@pytest.fixture(scope="class")
def parser():
    return Parser(_offset=1)


class TestParser:
    def test_parse(self, parser):
        filename, lineno, parsed_arguments, warning = parser.parse(None)

        assert filename == "tests/debugging/test_parser.py"
        assert lineno == 20
        assert parsed_arguments == [(None, None)]
        assert warning is None

    def test_parse_no_context(self, parser):  # pylint: disable=unused-argument
        filename, lineno, parsed_arguments, warning = eval("parser.parse(None)")  # pylint: disable=eval-used

        assert filename == "<string>"
        assert lineno == 1
        assert parsed_arguments == [(None, None)]
        assert warning == "error parsing code, no code context found"

    @patch("flashback.debugging.parser.get_frameinfo")
    def test_parse_exception(self, mocked_get_frameinfo, parser):
        mocked_get_frameinfo.side_effect = ValueError("call stack is not deep enough")

        filename, lineno, parsed_arguments, warning = parser.parse(None)

        assert filename == "<unknown>"
        assert lineno == 0
        assert parsed_arguments == [(None, None)]
        assert warning == "error parsing code, call stack is not deep enough (ValueError)"

    def test_parse_simple(self, parser):
        a = 1

        _, _, parsed_arguments, _ = parser.parse(a)

        assert parsed_arguments == [
            ("a", 1)
        ]

    def test_parse_multiple(self, parser):
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
            (None, False)
        ]

    def test_parse_complex(self, parser):
        a = {"a": 1, "b": 2, "c": 3}
        b = [i + 1 for i in range(3)]

        _, _, parsed_arguments, _ = parser.parse(a["a"], b, mock_function(1, 2), "a" if a else "b", 1 != 0)

        assert parsed_arguments == [
            ("a[\"a\"]", 1),
            ("b", [1, 2, 3]),
            ("mock_function(1, 2)", 3),
            ("\"a\" if a else \"b\"", "a"),
            ("1 != 0", True)
        ]

    def test_parse_no_space(self, parser):
        a = 1
        b = [1, 2, 3]
        c = {"a": 1, "b": 2, "c": 3}

        _, _, parsed_arguments, _ = parser.parse(a,b,c)

        assert parsed_arguments == [
            ("a", 1),
            ("b", [1, 2, 3]),
            ("c", {"a": 1, "b": 2, "c": 3})
        ]


    def test_parse_newline(self, parser):
        _, _, parsed_arguments, _ = parser.parse(
            1
        )
        assert parsed_arguments == [
            (None, 1)
        ]

    def test_parse_newlines(self, parser):
        _, _, parsed_arguments, warning = parser.parse(
            mock_function(
                1,
                2
            )
        )
        # Prior to python 3.8, the lineno for multiline calls is wrong
        if sys.version_info >= (3, 8):
            assert parsed_arguments == [
                ("mock_function(1, 2)", 3)
            ]
            assert warning is None
        else:
            assert parsed_arguments == [
                (None, 3)
            ]
            assert warning == "error parsing code, found ast.Num instead of ast.Call"

    def test_parse_nested_newlines(self, parser):
        _, _, parsed_arguments, warning = parser.parse(
            mock_function(
                mock_function(
                    mock_function(
                        mock_function(
                            1,
                            2
                        ),
                        3
                    ),
                    4
                ),
                5
            )
        )
        # Prior to python 3.8, the lineno for multiline calls is wrong
        if sys.version_info >= (3, 8):
            assert parsed_arguments == [
                ("mock_function(mock_function(mock_function(mock_function(1, 2), 3), 4), 5)", 15)
            ]
            assert warning is None
        else:
            assert parsed_arguments == [
                (None, 15)
            ]
            assert warning == "error parsing code, found ast.Num instead of ast.Call"
