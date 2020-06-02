# pylint: disable=no-self-use,redefined-outer-name

import os

import pytest

from flashback.importing import import_module_from_path


class TestImportModuleFromPath:
    def test_valid_module_valid_relative_path(self):
        import_module_from_path('dummy_module', path='.dummy_package')

        assert os.environ['DUMMY_ENV_VAR'] == 'dummy_value'

    def test_valid_module_valid_absolute_path(self):
        import_module_from_path('dummy_module', path='tests.importing.dummy_package')

        assert os.environ['DUMMY_ENV_VAR'] == 'dummy_value'

    def test_valid_module_valid_path_with_all(self):
        import_module_from_path('dummy_module', path='.dummy_package_with_all')

        assert os.environ['DUMMY_ENV_VAR'] == 'dummy_value'

    def test_valid_module_valid_toplevel_path(self):
        import_module_from_path('dummy_module', path='..importing.dummy_package')

        assert os.environ['DUMMY_ENV_VAR'] == 'dummy_value'

    def test_invalid_module_invalid_path(self):
        with pytest.raises(ImportError):
            import_module_from_path('invalid_module', path='.dummy_package')

    def test_valid_module_invalid_path(self):
        with pytest.raises(ImportError):
            import_module_from_path('dummy_module', path='.invalid_package')
