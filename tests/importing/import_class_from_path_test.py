import pytest

from flashback.importing import import_class_from_path


class ImportClassFromPathTest:
    def valid_class_valid_relative_path_test(self) -> None:
        cls = import_class_from_path("dummy_class", path=".dummy_package")

        assert isinstance(cls, object)

    def valid_class_valid_absolute_path_test(self) -> None:
        cls = import_class_from_path("dummy_class", path="tests.importing.dummy_package")

        assert isinstance(cls, object)

    def valid_class_valid_toplevel_path_test(self) -> None:
        cls = import_class_from_path("dummy_class", path="..importing.dummy_package")

        assert isinstance(cls, object)

    def invalid_class_invalid_path_test(self) -> None:
        with pytest.raises(ImportError):
            import_class_from_path("invalid_class", path=".invalid_package")

    def valid_class_invalid_path_test(self) -> None:
        with pytest.raises(ImportError):
            import_class_from_path("dummy_class", path=".invalid_package")

    def invalid_class_valid_path_test(self) -> None:
        with pytest.raises(AttributeError):
            import_class_from_path("mismatching_dummy_class", path=".dummy_package")
