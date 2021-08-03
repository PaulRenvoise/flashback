# pylint: disable=no-self-use,no-member,protected-access

import pytest

from flashback import Borg


def dummy_func(value, **kwargs):
    response = {"key": value}

    for attr, val in kwargs.items():
        response.update({attr: val})

    return response


@pytest.fixture(autouse=True)
def clean_up_shared_state():
    Borg._shared_state = {}


class TestBorg:
    def test_borg_functionnal(self):
        borg_1 = Borg()
        borg_2 = Borg()

        borg_1.assign_attribute("attr", 0)

        assert borg_1 != borg_2
        assert hasattr(borg_2, "attr")

    def test_borg_empty_dict(self):
        borg = Borg()

        assert borg.__dict__ == {}

    def test_assign_attribute(self):
        borg = Borg()

        borg.assign_attribute("attr_1", "foo")

        assert borg.attr_1 == "foo"

    def test_assign_attribute_override(self):
        borg = Borg()

        borg.assign_attribute("attr_1", "foo")

        assert borg.attr_1 == "foo"

        borg.assign_attribute("attr_1", "bar")

        assert borg.attr_1 == "foo"

    def test_assign_attribute_multiple(self):
        borg = Borg()

        borg.assign_attribute("attr_1", "foo")
        borg.assign_attribute("attr_2", dummy_func, "value", c="d")

        assert borg.attr_1 == "foo"
        assert borg.attr_2 == {"key": "value", "c": "d"}

    def test_assign_attributes(self):
        borg = Borg()

        borg.assign_attributes(
            attr_1="foo",
            attr_2=("foo", 1),
            attr_3=(dict, {"foo": 1}),
            attr_4=(dummy_func, "value"),
            attr_5=(dummy_func, "not_value", {"key": "value", "a": "b"}),
            attr_6=(dummy_func, "value", {"c": "d"})
        )

        assert borg.attr_1 == "foo"
        assert borg.attr_2 == ("foo", 1)
        assert borg.attr_3 == {"foo": 1}
        assert borg.attr_4 == {"key": "value"}
        assert borg.attr_5 == {"key": "value", "a": "b"}
        assert borg.attr_6 == {"key": "value", "c": "d"}

    def test_assign_attributes_override(self):
        borg = Borg()

        borg.assign_attributes(
            attr_1="foo",
            attr_2=("foo", 1),
            attr_3=(dict, {"foo": 1})
        )

        assert borg.attr_1 == "foo"
        assert borg.attr_2 == ("foo", 1)
        assert borg.attr_3 == {"foo": 1}

        borg.assign_attributes(
            attr_1="bar",
            attr_2=("bar", 2),
            attr_3=(dict, {"bar": 2})
        )

        assert borg.attr_1 == "foo"
        assert borg.attr_2 == ("foo", 1)
        assert borg.attr_3 == {"foo": 1}
