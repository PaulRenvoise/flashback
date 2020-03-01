# pylint: disable=no-self-use,redefined-outer-name

from copernicus.formatting import *


class TestCamelize():
    def test_lowercase(self):
        assert camelize('party') == 'Party'

    def test_snakecase(self):
        assert camelize('special_guest') == 'SpecialGuest'

    def test_camelcase(self):
        assert camelize('NotFunException') == 'NotFunException'

    def test_lowercase_and_acronyms(self):
        assert camelize('svcclassifier', acronyms=['SVC']) == 'SVCClassifier'

    def test_lowercase_and_weird_acronyms(self):
        assert camelize('https', acronyms=['HTTP']) == 'HTTPS'

    def test_lowercase_and_single_acronyms(self):
        assert camelize('http', acronyms=['HTTP']) == 'HTTP'

    def test_snakecase_and_acronyms(self):
        assert camelize('deep_custom_svc_classifier', acronyms=['DEep', 'SVC']) == 'DEepCustomSVCClassifier'

    def test_snakecase_and_weird_acronyms(self):
        assert camelize('application_controller', acronyms=['APP']) == 'APPLicationController'

    def test_lowercase_and_missing_acronyms(self):
        assert camelize('application', acronyms=['BSD']) == 'Application'

    def test_snakeize_revert(self):
        assert camelize(snakeize('SpecialGuest')) == 'SpecialGuest'

    def test_snakeize_revert_and_acronyms(self):
        acronyms = ['HTML']

        assert camelize(snakeize('HTMLTidyGenerator', acronyms=acronyms), acronyms=acronyms) == 'HTMLTidyGenerator'


class TestSnakeize():
    def test_lowercase(self):
        assert snakeize('party') == 'party'

    def test_snakecase(self):
        assert snakeize('special_guest') == 'special_guest'

    def test_camelcase(self):
        assert snakeize('NotFunException') == 'not_fun_exception'

    def test_lowercase_and_acronyms(self):
        assert snakeize('svcclassifier', acronyms=['SVC']) == 'svc_classifier'

    def test_snakecase_and_acronyms(self):
        assert snakeize('svc_classifier', acronyms=['SVC']) == 'svc_classifier'

    def test_snakecase_and_weird_acronyms(self):
        assert snakeize('application_controller', acronyms=['APP']) == 'app_lication_controller'

    def test_camelcase_and_acronyms(self):
        assert snakeize('SVCClassifier', acronyms=['SVC']) == 'svc_classifier'

    def test_camelcase_and_weird_acronyms(self):
        assert snakeize('HTTPS', acronyms=['HTTP']) == 'http_s'

    def test_lowercase_and_missing_acronyms(self):
        assert snakeize('https', acronyms=['BDS']) == 'https'

    def test_camelize_revert(self):
        assert snakeize(camelize('special_guest')) == 'special_guest'

    def test_camelize_revert_and_acronyms(self):
        acronyms = ['HTML']

        assert snakeize(camelize('html_tidy_generator', acronyms=acronyms), acronyms=acronyms) == 'html_tidy_generator'
