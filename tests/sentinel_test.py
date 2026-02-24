from flashback import Sentinel


class SentinelTest:
    def instance_equality_test(self) -> None:
        sentinel = Sentinel()

        assert sentinel == Sentinel()

    def instance_identity_test(self) -> None:
        sentinel = Sentinel()

        assert sentinel is Sentinel()

    def class_equality_test(self) -> None:
        sentinel = Sentinel()

        assert sentinel == Sentinel

    def class_identity_test(self) -> None:
        sentinel = Sentinel()

        assert sentinel is Sentinel
