from pygments.style import Style
from pygments.token import Comment, Generic, Keyword, Name, Number, \
                           Operator, Punctuation, Literal, String, Token


class Jellybeans(Style):
    """
    Implements the jellybeans.vim colorscheme for pygments.

    Inspired by:

    - https://github.com/cstrahan/pygments-styles/blob/master/themes/jellybeans.py
    """
    background_color = "#151515"

    styles = {
        Comment: "#888888",
        Comment.Hashbang: "",
        Comment.Multiline: "",
        Comment.Preproc: "#8fbfdc",
        Comment.Single: "",
        Comment.Special: "",

        Generic.Deleted: "#220000 bg:#220000",
        Generic.Error: "bg:#902020",
        Generic.Heading: "#70b950 bold",
        Generic.Inserted: "bg:#032218",
        Generic.Output: "#808080 bg:#151515",
        Generic.Subheading: "#70b950 bold",
        Generic.Traceback: "bg:#902020",

        Keyword: "#8197bf",
        Keyword.Constant: "#cf6a4c",
        Keyword.Namespace: "#8fbfdc",
        Keyword.Type: "#8fbfdc",

        Name.Attribute: "#fad07a",
        Name.Builtin.Pseudo: "#c6b6ee",
        Name.Builtin: "#fad07a",
        Name.Class: "#fad07a",
        Name.Constant: "#cf6a4c",
        Name.Decorator: "#fad07a",
        Name.Entity: "#799d6a",
        Name.Exception: "#8fbfdc",
        Name.Function: "#fad07a",
        Name.Label: "#ffb964",
        Name.Namespace: "",
        Name.Other: "",
        Name.Tag: "#8197bf",
        Name.Variable: "",

        Number: "#cf6a4c",
        Number.Bin: "",
        Number.Float: "",
        Number.Hex: "",
        Number.Integer.Long: "",
        Number.Integer: "",
        Number.Oct: "",

        Operator: "#8197bf",
        Operator.Word: "",

        Punctuation: "",

        Literal: "",
        Literal.Date: "",

        String: "#99ad6a",
        String.Affix: "",
        String.Backtick: "",
        String.Char: "",
        String.Delimiter: "",
        String.Doc: "",
        String.Double: "",
        String.Escape: "",
        String.Heredoc: "",
        String.Interpol: "",
        String.Other: "",
        String.Regex: "",
        String.Single: "",
        String.Symbol: "",

        Token: "#e8e8d3",
    }
