# pylint: disable=no-self-use

from flashback import Sentinel


class TestSentinel:
    def test_instance_equality(self):
        sentinel = Sentinel()

        assert sentinel == Sentinel()

    def test_instance_identity(self):
        sentinel = Sentinel()

        assert sentinel is Sentinel()

    def test_class_equality(self):
        sentinel = Sentinel()

        assert sentinel == Sentinel

    def test_class_identity(self):
        sentinel = Sentinel()

        assert sentinel is Sentinel
