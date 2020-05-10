import inspect


def get_frame(depth=0, context=1):
    """
    Finds the frame at `depth` and builds a FrameInfo from it.

    Executes 10 times faster than `inspect.stack()[depth]` if depth is
    superior to 1, else only 2 times.

    Handles negative `depth` by returning the current frame from the
    caller's perspective, just like `sys._getframe()` does.

    Params:
        - `depth (int)` the depth at which to find the frame
        - `context (int)` the number of lines surrounding the frame to use in the traceback of the frame

    Returns:
        - `inspect.FrameInfo`: the FrameInfo object for the frame

    Raises:
        - `ValueError` if `depth` is greater than the length of the call stack
    """
    # Could use `sys._getframe(1)` but safer to go through its wrapper
    frame = inspect.currentframe()
    # We need to skip the actual current frame (the execution of get_frame())
    depth = depth + 1 if depth > -1 else 1
    for _ in range(depth):
        if frame is None:
            raise ValueError('call stack is not deep enough')

        frame = frame.f_back

    if frame is None:
        raise ValueError('call stack is not deep enough')

    frameinfo = (frame,) + inspect.getframeinfo(frame, context)
    return inspect.FrameInfo(*frameinfo)
