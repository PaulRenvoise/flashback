import pytest
import typing as t

from flashback import classproperty


class ReadWrite(metaclass=classproperty.meta):
    _attribute = 0

    @classproperty
    def attribute(cls) -> t.Any:  # noqa: N805
        return cls._attribute

    @attribute.setter
    def attribute(cls, value: t.Any) -> None:  # noqa: N805
        cls._attribute = value


class ReadOnly(metaclass=classproperty.meta):
    _attribute = 0

    @classproperty
    def attribute(cls) -> t.Any:  # noqa: N805
        return cls._attribute


@pytest.fixture(autouse=True)
def _clean_up_class_attribute() -> None:
    ReadWrite.attribute = 0  # type: ignore because we use metaprog magic


class ClassPropertyTest:
    def readwrite_get_test(self) -> None:
        read_write = ReadWrite()

        assert read_write.attribute == 0

    def readwrite_set_test(self) -> None:
        read_write = ReadWrite()

        read_write.attribute = 1

        assert read_write.attribute == 1

    def readwrite_get_via_class_test(self) -> None:
        assert ReadWrite.attribute == 0

    def readwrite_set_via_class_test(self) -> None:
        read_write = ReadWrite()

        ReadWrite.attribute = 1  # type: ignore because we use metaprog magic

        assert read_write.attribute == 1

    def readonly_get_test(self) -> None:
        read_only = ReadOnly()

        assert read_only.attribute == 0

    def readonly_set_test(self) -> None:
        read_only = ReadOnly()

        with pytest.raises(AttributeError):
            read_only.attribute = 1

    def readonly_get_via_class_test(self) -> None:
        assert ReadOnly.attribute == 0

    def readonly_set_via_class_test(self) -> None:
        with pytest.raises(AttributeError):
            ReadOnly.attribute = 1  # type: ignore because we use metaprog magic
