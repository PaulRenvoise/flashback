from inspect import FrameInfo
from collections.abc import Callable

from flashback.debugging import get_callable, get_frameinfo


def dummy_function() -> FrameInfo:
    return get_frameinfo()


def dummy_closure() -> Callable[[], FrameInfo]:
    def _closure() -> FrameInfo:
        return get_frameinfo()

    return _closure


def dummy_nested_function() -> FrameInfo:
    def _nested_function() -> FrameInfo:
        return get_frameinfo()

    return _nested_function()


class DummyClass:
    def dummy_method(self) -> FrameInfo:
        return get_frameinfo()

    @classmethod
    def dummy_classmethod(cls) -> FrameInfo:
        return get_frameinfo()

    @staticmethod
    def dummy_staticmethod() -> FrameInfo:
        return get_frameinfo()


dummy_lambda = lambda: get_frameinfo()  # noqa: E731, PLW0108


class GetCallableTest:
    def function_test(self) -> None:
        frameinfo = dummy_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_function"

    def closure_test(self) -> None:
        frameinfo = dummy_closure()()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def nested_test(self) -> None:
        frameinfo = dummy_nested_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def lambda_test(self) -> None:
        frameinfo = dummy_lambda()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def method_test(self) -> None:
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_method()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_method"

    def classmethod_test(self) -> None:
        frameinfo = DummyClass.dummy_classmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_classmethod"

    def staticmethod_test(self) -> None:
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_staticmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None
