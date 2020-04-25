from pygments.style import Style
from pygments import token


class Solarized(Style):
    background_color = '#eee8d5'

    styles = {
        token.Text: 'bg: #eee8d5 #586e75',
        token.Keyword: '#859900',
        token.Keyword.Constant: 'bold',
        token.Keyword.Namespace: '#dc322f bold',
        token.Keyword.Type: 'bold',
        token.Name: '#268bd2',
        token.Name.Builtin: '#cb4b16',
        token.Name.Class: '#cb4b16',
        token.Name.Tag: 'bold',
        token.Literal: '#2aa198',
        token.Number: 'bold',
        token.Operator.Word: '#859900',
        token.Comment: '#93a1a1 italic',
        token.Generic: '#d33682',
    }
