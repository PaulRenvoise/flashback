from pygments.filters import Filter
from pygments.token import Name, Operator


class DecoratorOperatorFilter(Filter):
    """
    Extracts the '@' from a `pygments.token.Name.Decorator` to be a standalone
    `pygments.token.Operator`.
    """
    def __init__(self, **kwargs):
        """
        Params:
            kwargs (dict): every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

    def filter(self, lexer, stream):
        """
        Iterates over the stream of tokens and splits a `pygments.token.Name.Decorator: into two
        components.

        Some colorschemes handle the '@' as an operator, and the name of the decorator as a name,
        but pygments treat the whole thing as a decorator. This filter fixes this behaviour.

        Params:
            lexer (pygments.lexer.Lexer): the lexer instance
            stream (generator): the stream of couples tokentype-value

        Yields:
            tuple<pygments.token._TokenType, str>: the token type and token value
        """
        for ttype, value in stream:
            if ttype is Name.Decorator:
                yield Operator, '@'
                yield Name.Decorator, value[1:]
            else:
                yield ttype, value
