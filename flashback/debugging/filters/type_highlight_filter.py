from collections.abc import Iterable, Iterator
import typing as t

from pygments.lexer import Lexer
from pygments.filters import Filter
from pygments.token import Name, Keyword, _TokenType


class TypeHighlightFilter(Filter):
    """
    Modifies the token type of a Name token to Keyword.Type if its value appears in a list of values.
    """

    def __init__(self, names: list[str], **kwargs: t.Any) -> None:
        """
        Params:
            names: the list of names to change the token type
            kwargs: every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

        self.names = set(names)

    def filter(
        self,
        lexer: Lexer,  # noqa: ARG002
        stream: Iterable[tuple[_TokenType, str]],
    ) -> Iterator[tuple[_TokenType, str]]:
        """
        Iterates over the stream of tokens and modifies a token's type if its value appears in a
        list of names.

        Params:
            lexer: the lexer instance
            stream: the stream of couples tokentype-value

        Yields:
            the token type and token value
        """
        for token_type, value in stream:
            if token_type in Name and value in self.names:
                yield Keyword.Type, value
            else:
                yield token_type, value
