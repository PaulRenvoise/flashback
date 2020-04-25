from pygments.style import Style
from pygments import token


class Jellybeans(Style):
    background_color = '#151515'

    styles = {
        token.Token:              'noinherit #e8e8d3',
        token.Generic.Traceback:  'noinherit bg:#902020',
        token.Generic.Heading:    '#70b950 bold',
        token.Comment.Preproc:    'noinherit #8fbfdc',
        token.Name.Constant:      'noinherit #cf6a4c',
        token.Generic.Subheading: '#70b950 bold',
        token.Keyword:            'noinherit #8197bf',
        token.Name.Tag:           'noinherit #8197bf',
        token.Generic.Inserted:   'noinherit bg:#032218',
        token.Keyword.Type:       'noinherit #ffb964',
        token.Name.Variable:      'noinherit #c6b6ee',
        token.Generic.Deleted:    'noinherit #220000 bg:#220000',
        token.Number:             'noinherit #cf6a4c',
        token.Operator.Word:      'noinherit #e8e8d3 bg:#151515',
        token.Name.Function:      'noinherit #fad07a',
        token.Name.Entity:        'noinherit #799d6a',
        token.Name.Exception:     'noinherit #ffb964',
        token.Comment:            'noinherit #888888 italic',
        token.Generic.Output:     'noinherit #808080 bg:#151515',
        token.Name.Attribute:     'noinherit #fad07a',
        token.String:             'noinherit #99ad6a',
        token.Name.Label:         'noinherit #ffb964',
        token.Generic.Error:      'noinherit bg:#902020',
    }
