import inspect

def get_frameinfo(depth=0, context=1):
    """
    Finds the frame at `depth` and builds a `inspect.FrameInfo` from it.

    Executes 10 times faster than `inspect.stack()[depth]` if depth is superior to 1, else only 2
    times.

    Handles negative `depth` by returning the current frame from the caller's perspective, just
    like `sys._getframe()` does.

    Examples:
        ```python
        import inspect
        from flashback.debugging import get_frameinfo

        assert get_frameinfo() == inspect.stack()[0]

        def dummy_func():
            return get_frameinfo()

        frameinfo = dummy_func()
        assert frameinfo.function == "dummy_func"
        ```

    Params:
        depth (int): the depth at which to find the frame
        context (int): the number of lines surrounding the frame to use in the traceback

    Returns:
        inspect.FrameInfo: the FrameInfo object for the frame

    Raises:
        ValueError: if `depth` is greater than the length of the call stack
    """
    # Could use `sys._getframe(1)` but safer to go through its wrapper
    frame = inspect.currentframe()
    # Skips the actual current frame (the execution of get_frame())
    depth = depth + 1 if depth > -1 else 1
    for _ in range(depth):
        if frame is None:
            raise ValueError("call stack is not deep enough")

        frame = frame.f_back

    if frame is None:
        raise ValueError("call stack is not deep enough")

    frameinfo = (frame,) + inspect.getframeinfo(frame, context)
    return inspect.FrameInfo(*frameinfo)
