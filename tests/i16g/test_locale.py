# pylint: disable=no-self-use

import pytest
from mock import patch

from flashback.i16g import Locale


class TestLocale:
    def test_valid_locale(self):
        locale = Locale.load("en", path=".dummy_locales")

        assert locale.ID == "en"

    def test_valid_locale_with_territory(self):
        locale = Locale.load("fr_FR", path=".dummy_locales")

        assert locale.ID == "fr_fr"

    def test_inexistant_locale(self):
        with pytest.raises(NotImplementedError):
            Locale.load("zh_ZH.UTF-8", path=".dummy_locales")

    def test_invalid_locale(self):
        with pytest.raises(NotImplementedError):
            Locale.load("q", path=".dummy_locales")

    def test_incomplete_locale(self):
        with pytest.raises(NotImplementedError):
            Locale.load(".encoding@modifier", path=".dummy_locales")

    def test_invalid_folder(self):
        with pytest.raises(NotImplementedError):
            Locale.load("en", path=".")

    def test_cached_locale(self):
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
