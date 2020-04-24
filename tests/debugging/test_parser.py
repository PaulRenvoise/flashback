# pylint: disable=no-self-use,redefined-outer-name,invalid-name

import sys

import pytest
from mock import patch

from copernicus.debugging.parser import Parser

from .fixtures import mock_function


@pytest.fixture(scope='class')
def parser():
    return Parser(_offset=1)


class TestParser():
    def test_parse(self, parser):
        # We need to alias to xp to trick the Parser into finding the line (see CRE_XP in Parser)
        xp = parser.parse

        filename, lineno, parsed_arguments, warning = xp(None)

        assert filename == 'tests/debugging/test_parser.py'
        assert lineno == 23
        assert parsed_arguments == [(None, None)]
        assert warning is None

    def test_parse_no_statement(self, parser):
        ap = parser.parse

        filename, lineno, parsed_arguments, warning = ap(None)

        assert filename == 'tests/debugging/test_parser.py'
        assert lineno == 33
        assert parsed_arguments == [(None, None)]
        assert warning == 'error parsing code, xp call not found at line 33'

    def test_parse_no_context(self, parser):
        xp = parser.parse  # pylint: disable=unused-variable

        filename, lineno, parsed_arguments, warning = eval('xp(None)')  # pylint: disable=eval-used

        assert filename == '<string>'
        assert lineno == 1
        assert parsed_arguments == [(None, None)]
        assert warning == 'error parsing code, no code context found'

    @patch('inspect.stack')
    def test_parse_exception(self, mocked_inspect_stack, parser):
        xp = parser.parse

        mocked_inspect_stack.side_effect = TypeError('object is not a frame or traceback object')

        filename, lineno, parsed_arguments, warning = xp(None)

        assert filename == '<unknown>'
        assert lineno == 0
        assert parsed_arguments == [(None, None)]
        assert warning == 'error parsing code, object is not a frame or traceback object (TypeError)'

    def test_parse_simple(self, parser):
        xp = parser.parse

        a = 1

        _, _, parsed_arguments, _ = xp(a)

        assert parsed_arguments == [
            ('a', 1)
        ]

    def test_parse_multiple(self, parser):
        xp = parser.parse

        a = 1
        b = [1, 2, 3]
        c = {'a': 1, 'b': 2, 'c': 3}
        d = 'abc'

        _, _, parsed_arguments, _ = xp(a, b, c, d, False)

        assert parsed_arguments == [
            ('a', 1),
            ('b', [1, 2, 3]),
            ('c', {'a': 1, 'b': 2, 'c': 3}),
            ('d', 'abc'),
            (None, False)
        ]

    def test_parse_complex(self, parser):
        xp = parser.parse

        a = {'a': 1, 'b': 2, 'c': 3}
        b = [i + 1 for i in range(3)]

        _, _, parsed_arguments, _ = xp(a['a'], b, mock_function(1, 2), 'a' if a else 'b', 1 != 0)

        assert parsed_arguments == [
            ("a['a']", 1),
            ('b', [1, 2, 3]),
            ('mock_function(1, 2)', 3),
            ("'a' if a else 'b'", 'a'),
            ('1 != 0', True)
        ]

    def test_parse_no_space(self, parser):
        xp = parser.parse

        a = 1
        b = [1, 2, 3]
        c = {'a': 1, 'b': 2, 'c': 3}

        _, _, parsed_arguments, _ = xp(a,b,c)  # pylint: disable=bad-whitespace

        assert parsed_arguments == [
            ('a', 1),
            ('b', [1, 2, 3]),
            ('c', {'a': 1, 'b': 2, 'c': 3})
        ]


    def test_parse_newline(self, parser):
        xp = parser.parse

        _, _, parsed_arguments, _ = xp(
            1
        )
        assert parsed_arguments == [
            (None, 1)
        ]

    def test_parse_newlines(self, parser):
        xp = parser.parse

        _, _, parsed_arguments, warning = xp(
            mock_function(
                1,
                2
            )
        )
        if sys.version >= '3.8':
            assert parsed_arguments == [
                ('mock_function(1, 2)', 3)
            ]
            assert warning is None
        else:
            assert parsed_arguments is None
            assert warning == 'error parsing code, xp call not found at line 137'

    def test_parse_nested_newlines(self, parser):
        xp = parser.parse

        _, _, parsed_arguments, warning = xp(
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
        if sys.version >= '3.8':
            assert parsed_arguments == [
                ('mock_function(mock_function(mock_function(mock_function(1, 2), 3), 4), 5)', 15)
            ]
            assert warning is None
        else:
            assert parsed_arguments is None
            assert warning == 'error parsing code, xp call not found at line 137'
