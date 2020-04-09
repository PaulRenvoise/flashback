from abc import ABC, abstractmethod

class MockABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def mock_abstractmethod(self):
        pass
