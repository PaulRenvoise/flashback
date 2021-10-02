# pylint: disable=no-self-use,no-member,protected-access

import warnings

import pytest
from mock import Mock

from flashback import deprecated


def dummy_func(spy):
    spy.__call__()


@pytest.fixture(autouse=True)
def clean_up_dummy_func_doc():
    dummy_func.__doc__ = None


class TestDeprecated:
    def test_execution(self):
        spy_func = Mock()

        make_deprecated = deprecated(since="1.0", until="2.0", reason="that's life")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as _:
            decorated_func(spy_func)

            assert spy_func.called

    def test_message(self):
        spy_func = Mock()

        make_deprecated = deprecated()
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated."

    def test_message_with_since_and_until_and_reason(self):
        spy_func = Mock()

        make_deprecated = deprecated(since="1.0", until="2.0", reason="that's life")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated since 1.0 and will be removed in 2.0 because that's life."  # pylint: disable=line-too-long

    def test_message_with_since_and_reason(self):
        spy_func = Mock()

        make_deprecated = deprecated(since="1.0", reason="that's life")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated since 1.0 because that's life."

    def test_message_with_until_and_reason(self):
        spy_func = Mock()

        make_deprecated = deprecated(until="2.0", reason="that's life")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated and will be removed in 2.0 because that's life."  # pylint: disable=line-too-long

    def test_message_with_since_and_until(self):
        spy_func = Mock()

        make_deprecated = deprecated(since="1.0", until="2.0")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated since 1.0 and will be removed in 2.0."

    def test_message_with_since(self):
        spy_func = Mock()

        make_deprecated = deprecated(since="1.0")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated since 1.0."

    def test_message_with_until(self):
        spy_func = Mock()

        make_deprecated = deprecated(until="2.0")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated and will be removed in 2.0."

    def test_message_with_reason(self):
        spy_func = Mock()

        make_deprecated = deprecated(reason="that's life")
        decorated_func = make_deprecated(dummy_func)

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")

            decorated_func(spy_func)

            for warning in caught_warnings:
                if warning.category == DeprecationWarning:
                    assert str(warning.message) == "dummy_func is deprecated because that's life."

    def test_doc(self):
        make_deprecated = deprecated(since="1.0")
        make_deprecated(dummy_func)

        assert dummy_func.__doc__ == ".. deprecated:: dummy_func is deprecated since 1.0."

    def test_doc_append(self):
        dummy_func.__doc__ = "Initial doc"

        make_deprecated = deprecated(since="1.0")
        make_deprecated(dummy_func)

        assert dummy_func.__doc__ == "Initial doc\n\n.. deprecated:: dummy_func is deprecated since 1.0."
