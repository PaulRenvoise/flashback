from pygments.filters import Filter
from pygments.token import Name, Keyword


class TypeHighlightFilter(Filter):
    """
    Modifies the token type of a Name token to Keyword.Type if its value appears in a list of values.
    """
    def __init__(self, names, **kwargs):
        """
        Params:
            names (Iterable<str>): the list of names to change the token type
            kwargs (dict): every additional keyword parameters
        """
        Filter.__init__(self, **kwargs)

        self.names = set(names)

    def filter(self, lexer, stream):
        """
        Iterates over the stream of tokens and modifies a token's type if its value appears in a
        list of names.

        Params:
            lexer (pygments.lexer.Lexer): the lexer instance
            stream (generator): the stream of couples tokentype-value

        Yields:
            tuple<pygments.token._TokenType, str>: the token type and token value
        """
        for ttype, value in stream:
            if ttype in Name and value in self.names:
                yield Keyword.Type, value
            else:
                yield ttype, value
