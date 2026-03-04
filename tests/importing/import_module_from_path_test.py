import os

import pytest

from flashback.importing import import_module_from_path


class ImportModuleFromPathTest:
    def valid_module_valid_relative_path_test(self) -> None:
        import_module_from_path("dummy_module", path=".dummy_package")

        assert os.environ["DUMMY_ENV_VAR"] == "dummy_value"

    def valid_module_valid_absolute_path_test(self) -> None:
        import_module_from_path("dummy_module", path="tests.importing.dummy_package")

        assert os.environ["DUMMY_ENV_VAR"] == "dummy_value"

    def valid_module_valid_path_with_all_test(self) -> None:
        import_module_from_path("dummy_module", path=".dummy_package_with_all")

        assert os.environ["DUMMY_ENV_VAR"] == "dummy_value"

    def valid_module_valid_toplevel_path_test(self) -> None:
        import_module_from_path("dummy_module", path="..importing.dummy_package")

        assert os.environ["DUMMY_ENV_VAR"] == "dummy_value"

    def invalid_module_invalid_path_test(self) -> None:
        with pytest.raises(ImportError):
            import_module_from_path("invalid_module", path=".dummy_package")

    def valid_module_invalid_path_test(self) -> None:
        with pytest.raises(ImportError):
            import_module_from_path("dummy_module", path=".invalid_package")
