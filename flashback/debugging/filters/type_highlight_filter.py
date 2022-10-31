from typing import Any, Generator, Iterable, Tuple

import pygments  # type: ignore
from pygments.filters import Filter  # type: ignore
from pygments.token import Name, Keyword  # type: ignore


class TypeHighlightFilter(Filter):
    """
    Modifies the token type of a Name token to Keyword.Type if its value appears in a list of values.
    """
    def __init__(self, names: Iterable[str], **kwargs: Any) -> None:
        """
        Params:
            names: the list of names to change the token type
            kwargs: every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

        self.names = set(names)

    def filter(self, lexer: pygments.lexer.Lexer, stream: Generator) -> Generator[Tuple[pygments.token._TokenType, str], None, None]:
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
