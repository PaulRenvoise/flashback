from flashback.debugging import get_callable, get_frameinfo


def dummy_function():
    return get_frameinfo()


def dummy_closure():
    def _closure():
        return get_frameinfo()

    return _closure


def dummy_nested_function():
    def _nested_function():
        return get_frameinfo()

    return _nested_function()


class DummyClass:
    def dummy_method(self):
        return get_frameinfo()

    @classmethod
    def dummy_classmethod(cls):
        return get_frameinfo()

    @staticmethod
    def dummy_staticmethod():
        return get_frameinfo()


dummy_lambda = lambda: get_frameinfo()  # noqa: E731


class TestGetCallable:
    def test_function(self):
        frameinfo = dummy_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_function"

    def test_closure(self):
        frameinfo = dummy_closure()()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_nested(self):
        frameinfo = dummy_nested_function()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_lambda(self):
        frameinfo = dummy_lambda()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is None

    def test_method(self):
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_method()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_method"

    def test_classmethod(self):
        frameinfo = DummyClass.dummy_classmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance.__name__ == "dummy_classmethod"

    def test_staticmethod(self):
        dummy_class = DummyClass()
        frameinfo = dummy_class.dummy_staticmethod()

        callable_instance = get_callable(frameinfo)

        assert callable_instance is not None
        assert callable_instance is None
