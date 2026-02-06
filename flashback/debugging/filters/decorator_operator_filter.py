from collections.abc import Iterable, Iterator
import typing as t

from pygments.filters import Filter
from pygments.token import Name, Operator, _TokenType
from pygments.lexer import Lexer


class DecoratorOperatorFilter(Filter):
    """
    Extracts the '@' from a `pygments.token.Name.Decorator` to be a standalone
    `pygments.token.Operator`.
    """

    def __init__(self, **kwargs: t.Any) -> None:
        """
        Params:
            kwargs: every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

    def filter(
        self,
        lexer: Lexer,  # noqa: ARG002
        stream: Iterable[tuple[_TokenType, str]],
    ) -> Iterator[tuple[_TokenType, str]]:
        """
        Iterates over the stream of tokens and splits a `pygments.token.Name.Decorator: into two
        components.

        Some colorschemes handle the '@' as an operator, and the name of the decorator as a name,
        but pygments treat the whole thing as a decorator. This filter fixes this behaviour.

        Params:
            lexer: the lexer instance
            stream: the stream of couples tokentype-value

        Yields:
            the token type and token value
        """
        for token_type, value in stream:
            if token_type is Name.Decorator:
                yield Operator, "@"
                yield Name.Decorator, value[1:]
            else:
                yield token_type, value
