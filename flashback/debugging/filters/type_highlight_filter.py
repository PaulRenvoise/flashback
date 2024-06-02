from __future__ import annotations

from collections.abc import Generator

from pygments.lexer import Lexer
from pygments.filters import Filter
from pygments.token import Name, Keyword, _TokenType


class TypeHighlightFilter(Filter):
    """
    Modifies the token type of a Name token to Keyword.Type if its value appears in a list of values.
    """

    def __init__(self, names: list[str], **kwargs) -> None:
        """
        Params:
            names: the list of names to change the token type
            kwargs: every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

        self.names = set(names)

    def filter(self, _lexer: Lexer, stream: Generator) -> Generator[tuple[_TokenType, str], None, None]:
        """
        Iterates over the stream of tokens and modifies a token's type if its value appears in a
        list of names.

        Params:
            lexer: the lexer instance
            stream: the stream of couples tokentype-value

        Yields:
            the token type and token value
        """
        for ttype, value in stream:
            if ttype in Name and value in self.names:
                yield Keyword.Type, value
            else:
                yield ttype, value
