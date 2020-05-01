# pylint: disable=no-self-use,no-member,protected-access,no-self-argument

import pytest

from flashback import classproperty


class ReadWrite(metaclass=classproperty.meta):
    _attribute = 0

    @classproperty
    def attribute(cls):
        return cls._attribute

    @attribute.setter
    def attribute(cls, value):
        cls._attribute = value

class ReadOnly(metaclass=classproperty.meta):
    _attribute = 0

    @classproperty
    def attribute(cls):
        return cls._attribute


@pytest.fixture(autouse=True)
def clean_up_class_attribute():
    ReadWrite.attribute = 0


class TestClassProperty:
    def test_readwrite_get(self):
        read_write = ReadWrite()

        assert read_write.attribute == 0

    def test_readwrite_set(self):
        read_write = ReadWrite()

        read_write.attribute = 1

        assert read_write.attribute == 1

    def test_readwrite_get_via_class(self):
        assert ReadWrite.attribute == 0

    def test_readwrite_set_via_class(self):
        read_write = ReadWrite()

        ReadWrite.attribute = 1

        assert read_write.attribute == 1

    def test_readonly_get(self):
        read_only = ReadOnly()

        assert read_only.attribute == 0

    def test_readonly_set(self):
        read_only = ReadOnly()

        with pytest.raises(AttributeError):
            read_only.attribute = 1

    def test_readonly_get_via_class(self):
        assert ReadOnly.attribute == 0

    def test_readonly_set_via_class(self):
        with pytest.raises(AttributeError):
            ReadOnly.attribute = 1
