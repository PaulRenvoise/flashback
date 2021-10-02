def get_callable(frameinfo):
    """
    Finds the callable being executed during the given `frameinfo`.

    Starts by using the co_name found in the frame, then looks for a 'self' or 'cls' in the
    locals (in this case, callable is a method). If no class object or instance exists, looks
    into the frameinfo's globals (in that case, callable is just a function).

    Note, as of 12/05/2020:
    - Static methods are not found neither in locals nor globals, and they're
    not bound to a class or instance.
    - Closures and nested functions are not found neither in locals nor globals.
    - Lambdas exists in globals, but they're named as '<lambda>' in co_name, so we can't find them.

    Examples:
        ```python
        from flashback.debugging import get_frameinfo, get_callable

        def dummy_func():
            return get_frameinfo()

        frameinfo = dummy_func()

        assert get_callable(frameinfo) == dummy_func

        class DummyClass():
            def dummy_method(self):
                return get_frameinfo()

            @classmethod
            def dummy_classmethod(cls):
                return get_frameinfo()

        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_method()

        assert get_callable(frameinfo) == dummy_class.dummy_method

        frameinfo = DummyClass.dummy_classmethod()

        assert get_callable(frameinfo) == DummyClass.dummy_classmethod
        ```

    Params:
        frameinfo (inspect.FrameInfo): the frameinfo to extract the callable from

    Returns:
        Callable|None: the callable instance if found
    """
    frame = frameinfo.frame

    function_name = frame.f_code.co_name

    caller_class = frame.f_locals.get("self", None)
    if caller_class is None:
        caller_class = frame.f_locals.get("cls", None)

    caller_instance = getattr(caller_class, function_name, None)
    if caller_instance is None:
        caller_instance = frame.f_globals.get(function_name, None)

    return caller_instance
