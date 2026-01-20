from abc import ABC, abstractmethod


class MockABC(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def mock_abstractmethod(self) -> None:
        pass
