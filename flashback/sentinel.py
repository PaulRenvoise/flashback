class Sentinel:
    """
    Implements a class useful to create a Sentinel design pattern.

    Examples:
        ```python
        from flashback import Sentinel

        sentinel = Sentinel()
        dummy = sentinel

        # Equals itself
        assert sentinel == dummy

        # But also its class
        assert sentinel == Sentinel

        # Because it IS its class
        assert sentinel is Sentinel

        # Quick example of usage
        iterable = ["abc", None, "xyz", sentinel]
        for item in iterable:
            if item is Sentinel:
                raise StopIteration
            print(item)
        #=> "abc"
        #=> None
        #=> "xyz"
        #=> StopIteration
        ```
    """
    def __new__(cls):
        return cls
