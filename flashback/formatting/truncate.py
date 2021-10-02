def truncate(text, limit=120, suffix="..."):
    """
    Truncates the given text up to `limit` and fill its ending with `suffix`.

    Tries to find the latest space before the `limit` which is located in the second half of the
    text. If no space is found, truncates at the limit. Searching for a space in the second-half
    of the text avoids cases where the word going over the limit is very long, e.g.:

    ```python
    # Without:
    truncate("I spectrophotofluorometrically assessed this sample", limit=25)
    #=> "I..."

    # With:
    truncate("I spectrophotofluorometrically assessed this sample", limit=25)
    #=> "I spectrophotofluorom..."
    ```

    Adapted from https://github.com/reddit/reddit/blob/master/r2/r2/lib/utils/utils.py#L407.

    Examples:
        ```python
        from flashback.formatting import truncate

        truncate("This helper is very useful for preview of descriptions", limit=50)
        #=> "This helper is very useful for preview of..."

        truncate("Wonderful tool to use in any projects!", limit=35, suffix=", bla bla bla")
        #=> "Wonderful tool to use, bla bla bla"

        truncate("Hi there", limit=3, suffix="")
        #=> "Hi"
        ```

    Params:
        text (str): the text to truncate
        limit (int): the maximum length of the text
        suffix (str): the suffix to append at the truncated text

    Returns
        str: the truncated text
    """
    if len(text) <= limit:
        return text

    truncated_text = text[:(limit - len(suffix))]
    try:
        space_index = truncated_text.rindex(" ")
    except ValueError:
        space_index = -1

    if space_index < limit // 2:
        space_index = -1

    return truncated_text[:space_index] + suffix
