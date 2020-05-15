# pylint: disable=no-self-use,redefined-outer-name

import pytest

from flashback.importing import import_class_from_path


class TestImportClassFromPath:
    def test_valid_class_valid_relative_path(self):
        cls = import_class_from_path('dummy_class', path='.dummy_package')

        assert isinstance(cls, object)

    def test_valid_class_valid_absolute_path(self):
        cls = import_class_from_path('dummy_class', path='tests.importing.dummy_package')

        assert isinstance(cls, object)

    def test_valid_class_valid_toplevel_path(self):
        cls = import_class_from_path('dummy_class', path='..importing.dummy_package')

        assert isinstance(cls, object)

    def test_invalid_class_invalid_path(self):
        with pytest.raises(ImportError):
            import_class_from_path('invalid_class', path='.invalid_package')

    def test_valid_class_invalid_path(self):
        with pytest.raises(ImportError):
            import_class_from_path('dummy_class', path='.invalid_package')

    def test_invalid_class_valid_path(self):
        with pytest.raises(AttributeError):
            import_class_from_path('mismatching_dummy_class', path='.dummy_package')
