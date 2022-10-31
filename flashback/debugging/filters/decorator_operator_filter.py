from typing import Any, Generator, Tuple

import pygments  # type: ignore
from pygments.filters import Filter  # type: ignore
from pygments.token import Name, Operator  # type: ignore


class DecoratorOperatorFilter(Filter):
    """
    Extracts the '@' from a `pygments.token.Name.Decorator` to be a standalone
    `pygments.token.Operator`.
    """
    def __init__(self, **kwargs: Any)  -> None:
        """
        Params:
            kwargs: every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

    def filter(self, lexer: pygments.lexer.Lexer, stream: Generator) -> Generator[Tuple[pygments.token._TokenType, str], None, None]:
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
        for ttype, value in stream:
            if ttype is Name.Decorator:
                yield Operator, '@'
                yield Name.Decorator, value[1:]
            else:
                yield ttype, value
