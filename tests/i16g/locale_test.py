from unittest.mock import patch

import pytest

from flashback.i16g import Locale


class LocaleTest:
    def valid_locale_test(self) -> None:
        locale = Locale.load("en", path=".dummy_locales")

        assert locale.ID == "en"

    def valid_locale_with_territory_test(self) -> None:
        locale = Locale.load("fr_FR", path=".dummy_locales")

        assert locale.ID == "fr_fr"

    def inexistant_locale_test(self) -> None:
        with pytest.raises(NotImplementedError):
            Locale.load("zh_ZH.UTF-8", path=".dummy_locales")

    def invalid_locale_test(self) -> None:
        with pytest.raises(NotImplementedError):
            Locale.load("q", path=".dummy_locales")

    def incomplete_locale_test(self) -> None:
        with pytest.raises(NotImplementedError):
            Locale.load(".encoding@modifier", path=".dummy_locales")

    def invalid_folder_test(self) -> None:
        with pytest.raises(NotImplementedError):
            Locale.load("en", path=".")

    def cached_locale_test(self) -> None:
        with patch("flashback.i16g.locale.import_module") as mock:
            mock.return_value = True

            Locale.load("es", path=".dummy_locales")

            # We expect to load the module the first time
            assert mock.called

        with patch("flashback.i16g.locale.import_module") as mock:
            mock.return_value = True

            Locale.load("es", path=".dummy_locales")

            # But not the second time
            assert not mock.called
